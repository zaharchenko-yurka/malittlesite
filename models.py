from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


site = Flask(__name__)
site.config['SECRET_KEY'] = 'sd&^*%59SA5(*&egflaLK:Jfa;jfc;oWCVahnp'
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(site)

class Features(db.Model):
    __tablename__ = "features"

    feature_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    type = db.Column(db.String(30))
    longitude = db.Column(db.String(16))
    latitude = db.Column(db.String(16))
    active = db.Column(db.Boolean, default = True)

    def __str__ (self):
        return '''
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates":  [ ''' + self.longitude + ',' + self.latitude + ''' ]
        },
        "properties": {
        "name": "''' + self.name + '''",
        "description": "''' + self.description + '''"
        }
    }'''

class Users(db.Model, UserMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(16))
    active = db.Column(db.Boolean, default = False)
    email = db.Column(db.String(100), nullable = False)

    def __repr__(self):
	    return "<{}:{}>".format(self.user_id, self.username)

    def set_password(self, passwordy):
	    self.password = generate_password_hash(passwordy)

    def check_password(self,  passwordy):
	    return check_password_hash(self.password, passwordy)

    def get_id(self):
        return str(self.user_id)

class Message(db.Model):
    __tablename__ = "message"

    message_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    message = db.Column(db.Text)
    username = db.Column(db.String(32))
    contact = db.Column(db.String(32))
    longitude = db.Column(db.String(16), nullable = False)
    latitude = db.Column(db.String(16), nullable = False)
    zoom = db.Column(db.String(2))
