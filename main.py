from flask import Flask, render_template, request, make_response

from models import site, db, Features, Message, Users
from admin.admin import admin
from utils import get_geojson


#db.init_app(site)

site.register_blueprint(admin, url_prefix='/admin')

main_menu = [
    {'name': 'Новини', 'url': 'news'},
    {'name': 'ЧаПи', 'url': 'faq'}
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
        try:
            msg = Message(name = request.form['name'],
                        message = request.form['message'],
                        username = request.form['username'],
                        contact = request.form['contact'],
                        longitude = request.form['longitude'],
                        latitude = request.form['latitude'],
                        zoom = request.form['zoom'])
            db.session.add(msg)
            db.session.commit()
            site.logger.info('Мєссагу успішно записано до БД')
        except:
            db.session.rollback()
            site.logger.error('Шось не то з БД - повідомлення від користувача не додано')
        return '201'
    else:
        return render_template('index.html', main_menu=main_menu), 200

@site.errorhandler(404)
def page404(error):
    return render_template('page404.html', main_menu=main_menu), 404

@site.route('/markers')
def markers():
    """Формує динамічний markers.geojson із таблиці features в базі даних.
    """
    features_list = []
    types = ['sanctuarys', 'old', 'museums', 'etno', 'spring', 'stones', 'trees', 'attraction']
    for feature_type in types:
        features_list.append(feature_type)
        features = Features.query.filter_by(type=feature_type, active='true').all()
        features_list.append(features)

    resp = make_response(get_geojson(features_list=features_list))
    resp.headers['Content-Type'] = 'application/geojson'
    return resp

if __name__ == '__main__':
    site.run(debug=True)
