# first file that runs , db , instance , login 
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import  Api
db= SQLAlchemy()


app = Flask(__name__)
api=Api(app)


app.config['SECRET_KEY']='secretkey'
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False    
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


from .models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




#connecting the pages 
from .main import mainB 
from .auth import authB
from .todoapi import todoapiB
app.register_blueprint(mainB)
app.register_blueprint(authB)
app.register_blueprint(todoapiB)




Migrate(app,db)







