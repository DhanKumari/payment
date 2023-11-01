from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db


authB = Blueprint('auth',__name__)

@authB.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        email= request.form.get('email')
        name= request.form.get('name')
        password= request.form.get('password')

        #print(email,name,password)

        user = User.query.filter_by(email=email).first()
        if user:
            return " already present "


        new_user = User(email=email, name=name, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
  
    return render_template('signup.html')



@authB.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password= request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password,password):
            return redirect('auth.login')
        
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    
    return render_template('login.html')



@authB.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))