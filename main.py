import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, make_response

site = Flask(__name__)
site.config['SECRET_KEY'] = 'sd&^*%59SA5(*&egflaLK:Jfa;jfc;oWCVahnp'

main_menu = [
    {'name': 'Новини', 'url': 'news'},
    {'name': 'Про нас', 'url': 'about'},
    {'name': 'Увійти', 'url': 'login'},
    {'name': 'Вийти', 'url': 'logout'}
]

@site.route('/index')
@site.route('/home')
@site.route('/', methods = ['POST', 'GET'])
def index():
    """Віддаємо головну сторінку, приймаємо повідомлення із форми, пишемо їх в базу даних.

    Returns:
        index.html або код '201'
    """
    if request.method == "POST":
        with sqlite3.connect('instance/site.db') as db:
            cur = db.cursor()
            message = (request.form['name'], request.form['message'], request.form['username'],
                        request.form['contact'], request.form['longitude'], request.form['latitude'],
                        request.form['zoom'])
            cur.execute("""INSERT INTO message
                        (name, message, username, contact, longitude, latitude, zoom)
                        VALUES (?,?,?,?,?,?,?)""", message)
        return '201'
    else:
        return render_template('index.html', main_menu=main_menu), 200

@site.errorhandler(404)
def page404(error):
    return render_template('page404.html', main_menu=main_menu), 404

@site.route('/login', methods = ['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect('/admin')
    elif request.method == 'POST':
        with sqlite3.connect('instance/site.db') as db:
            cur = db.cursor()
            cur.execute(f"""--sql SELECT password, active FROM users
                        WHERE username = '{request.form['username']}'
                        """)
            password, active = cur.fetchone()
        if password == request.form['password'] and active:
            session['userLogged'] = request.form['username']
            main_menu[2] = {'name': 'Адмінка', 'url': 'admin'}
            return redirect(url_for('admin'))
    else:
        return render_template('login.html', main_menu=main_menu), 200
    
@site.route('/admin')
def admin():
    if 'userLogged' not in session:
        return redirect(url_for('index'))
    else:
        return 'Йа адмінко!'

@site.route('/logout') # чось не працює...
def logout():
    # remove the username from the session if it's there
    session.pop(session['userLogged'], None)
    return redirect(url_for('index'))

@site.route('/markers')
def markers():
    features_list = []
    types = ['sanctuarys', 'old', 'museums', 'etno', 'spring', 'stones', 'trees', 'attraction']
    with sqlite3.connect('instance/site.db') as db:
        cur = db.cursor()
        for feature_type in types:
            features_list.append(feature_type)
            cur.execute(f"""SELECT longitude, latitude, name, description
                       FROM features
                       WHERE type = '{feature_type}' AND active = 'true'""")
            features = cur.fetchall()
            features_list.append(features)
            #  отримуємо список: ['тип_маркера', [('широта', 'довгота', 'назва', 'опис'), (), 'наступний_тип_маркера' ...], ... ]
    global_flag = False
    markers_geojson = 'var '
    for i in range(0, len(features_list), 2):
        if global_flag:             # Кома у кінці файлу. Пишемо її на початку, щоб не видаляти після останньої позиції
            markers_geojson += ''',
'''                                 # пропускаємо перед першим входженням
        else:
            global_flag = True
        markers_geojson += features_list[i] + ''' = {
    "type": "FeatureCollection",
    "features": ['''
        if features_list[i+1]:
            flag = False
            for feature in features_list[i+1]:
                if flag:                    # Кома, що розділяє словники з окремими позначками
                    markers_geojson += ''', ''' # пропускаємо перед першим входженням
                else:
                    flag = True
                markers_geojson += '''
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates":  [ ''' + feature[0] + ',' + feature[1] + ''' ]
        },
        "properties": {
        "name": "''' + feature[2] + '''",
        "description": "''' + feature[3] + '''"
        }
    }'''
        markers_geojson += ''']
}'''
    resp = make_response(markers_geojson)
    resp.headers['Content-Type'] = 'application/geojson'
    return resp

if __name__ == '__main__':
    site.run(debug=True)
