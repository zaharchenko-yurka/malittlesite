from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/login', methods = ['POST', 'GET'])
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
    
@admin.route('/admin')
def admin():
    if 'userLogged' not in session:
        return redirect(url_for('index'))
    else:
        return 'Йа адмінко!'