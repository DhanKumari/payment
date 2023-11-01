#create , update , delete, post
#blueprint: organise the files

from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from .models import Workout, User
from youtube import db

mainB = Blueprint('main',__name__)

@mainB.route('/')
def index():
    return render_template('index.html')

@mainB.route('/profile')
@login_required
def profile():

    return render_template('profile.html', name=current_user.name)

#create
@mainB.route('/newworkout', methods=['GET','POST'])
@login_required
def new_workout():
    if request.method=='POST':
        pushup = request.form.get('pushup')
        comment=request.form.get('comment')
        workout= Workout(pushup=pushup,comment=comment,author=current_user)
        db.session.add(workout)
        db.session.commit()

        flash('your workout has been added ')
        return redirect(url_for('main.user_workouts'))
    return render_template('create_workout.html')

#get, pagination
@mainB.route('/all')
@login_required
def user_workouts():
    page=request.args.get('page',1, type=int)
    user= User.query.filter_by(email=current_user.email).first_or_404()
    #workouts = user.workouts
    workouts = Workout.query.filter_by(author=user).paginate(page=page,per_page=3)
    #print(workouts)

    return render_template('all_workouts.html', workouts=workouts,user=user)

#update
@mainB.route('/workout/<int:workout_id>/update', methods=['GET','POST'])
@login_required
def update_workout(workout_id):
    workout =Workout.query.get_or_404(workout_id)

    if request.method == 'POST':
        workout.pushup= request.form['pushup']
        workout.comment=request.form['comment']
        db.session.commit()
        flash('your workout has been updated ')
        return redirect(url_for('main.user_workouts'))


    return render_template('update_workout.html',workout=workout)


#delete
@mainB.route('/workout/<int:workout_id>/delete', methods=['GET','POST'])
@login_required
def delete_workout(workout_id):
    workout =Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('deleted ')

    return redirect(url_for('main.user_workouts'))
#return user to all workout 
