from flask import Flask, render_template, request, redirect
import sqlite3

site = Flask(__name__)

main_menu = [
    {'name': 'Новини', 'url': 'news'},
    {'name': 'Про нас', 'url': 'about'},
    {'name': 'Увійти', 'url': 'login'}
]

@site.route('/index')
@site.route('/home')
@site.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        with sqlite3.connect('instance/site.db') as db:
            cur = db.cursor()
            message = (request.form['name'], request.form['message'], request.form['username'], request.form['contact'],
                        request.form['longitude'], request.form['latitude'], request.form['zoom'])
            cur.execute('''INSERT INTO message
                        (name, message, username, contact, longitude, latitude, zoom)
                        VALUES (?,?,?,?,?,?,?)''', message)
        return '201'
    else:
        return render_template('index.html', main_menu=main_menu)

# @site.route('/login', methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = db.session.execute(db.select(Users).filter_by(username=request.form['username']))

if __name__ == '__main__':
    site.run(debug=True)
