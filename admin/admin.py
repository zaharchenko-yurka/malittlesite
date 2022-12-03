from flask import Blueprint, session, redirect, url_for
from forms import *
from models import db, Users

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

admin_menu = [
    {'name': 'Записи', 'url': 'features'},
    {'name': 'Користувачі', 'url': 'users'},
    {'name': 'Новини', 'url': 'news'},
    {'name': 'ЧаПи', 'url': 'faq'}
]

@admin.route('/login', methods = ['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect('/')
    elif request.method == 'POST':
        with sqlite3.connect('instance/site.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT password, active FROM users
                        WHERE username = '{request.form['username']}'
                        """)
            password, active = cur.fetchone()
        if password == request.form['password'] and active:
            session['userLogged'] = request.form['username']
            return redirect(url_for('/'))
    else:
        return render_template('login.html', admin_menu=admin_menu), 200
    
@admin.route('/')
def adminka():
    if 'userLogged' not in session:
        return redirect(url_for('/login'))
    else:
        return 'Йа адмінко!'