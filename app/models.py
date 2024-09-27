from .extensions import db
from flask_login import UserMixin

class Device(db.Model):
    assignee = db.Column(db.String(16), db.ForeignKey('user.username'))
    dsn = db.Column(db.String(16), primary_key=True)
    program = db.Column(db.String(100))
    location_code = db.Column(db.String(10))
    condition = db.Column(db.String(100))
    last_updated = db.Column(db.String(20))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(256))
    devices = db.relationship('Device')
