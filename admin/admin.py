from flask import Blueprint, redirect, url_for, render_template
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

from admin.forms import *
from models import site, db, Users
from admin.requires import admin_required, moderator_required

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

login_manager = LoginManager(site)
login_manager.login_view = 'admin.login' #  визначає функцію подання для перенаправлення неавторизованих користувачів для авторизації
login_manager.login_message = 'Будь ласочка, авторизуйтесь'

admin_menu = [
    {'name': 'Записи', 'url': '/admin'},
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
        return render_template('admin/login.html', form=form)

@admin.route('/register', methods = ['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.adminka'))
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            new_user = Users(username=form.user_name.data, email=form.email.data, active=False, role='cadet')
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
            site.logger.error('Помилка запису БД')
            return redirect(url_for('admin.login'))
        site.logger.info('Зареєстрований!')
        return redirect(url_for('admin.adminka'))
    else:
        return render_template('admin/register.html', form=form)

@admin.route('/')
@moderator_required # https://flask-user.readthedocs.io/en/v0.6/authorization.html
def adminka():
    return render_template('admin/adminka.html', menu=admin_menu)

@admin.route('/news')
@admin_required
def news():
    return render_template('admin/news.html', menu=admin_menu)

@admin.route('/faq')
@admin_required
def faq():
    return render_template('admin/faq.html', menu=admin_menu)

@admin.route('forgot_password')
def forgot_password():
    pass

@admin.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
