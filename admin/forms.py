from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField(description="E-mail", validators=[Email("Невірний формат e-mail")])
    password = PasswordField(description="Пароль", validators=[DataRequired(), Length(min=6, max=100, message='Пароль має бути не коротше 6 символів')])
    remember_me = BooleanField("Запам'ятати мене", default=False)
    submit = SubmitField("Вхід")

class RegisterForm(FlaskForm):
    user_name = StringField("Користувач: ", validators=[DataRequired("Назвіть себе, бо якось невдобно")])
    email = StringField("E-mail: ", validators=[Email("Невірний формат e-mail")])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=6, max=100, message='Пароль має бути не коротше 6 символів')])
    pas_verification = PasswordField("Пароль: ", validators=[EqualTo('password', 'Паролі не збігаються')])
    submit = SubmitField("Надіслати")
