from .import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = db.Column(db.Integer,primary_key=True)
    email= db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    name= db.Column(db.String(100), nullable=False)
    workouts = db.relationship('Workout', backref='author', lazy=True)

class Workout(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    pushup=db.Column(db.Integer)
    date_posted= db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    comment = db.Column(db.Text,nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)


class TodoModel(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))


