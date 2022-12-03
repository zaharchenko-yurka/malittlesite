from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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

class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(16))
    active = db.Column(db.Boolean, default = False)
    email = db.Column(db.String(100), nullable = False)

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