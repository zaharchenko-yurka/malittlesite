from flask import Blueprint, redirect, url_for, render_template
from flask_login import LoginManager, login_required, login_user, current_user

from admin.forms import *
from models import site, db, Users

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

login_manager = LoginManager(site)
login_manager.login_view = 'admin.login' #  визначає функцію подання для перенаправлення неавторизованих користувачів для авторизації
login_manager.login_message = 'Будь ласочка, авторизуйтесь'

admin_menu = [
    {'name': 'Записи', 'url': 'features'},
    {'name': 'Користувачі', 'url': 'users'},
    {'name': 'Новини', 'url': 'news'},
    {'name': 'ЧаПи', 'url': 'faq'}
]

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)

@admin.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.adminka'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, active=True).first()
        site.logger.info(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            site.logger.info('Log in successfully')
            return redirect(url_for('admin.adminka'))
        else:
            return redirect(url_for('admin.login'))
    else:
        return render_template('admin/login.html', admin_menu=admin_menu, form=form)

@admin.route('/register')
def register():
    pass

@admin.route('/')
@login_required
def adminka():
        return 'Йа адмінко!'

@admin.route('forgot_password')
def forgot_password():
    pass
