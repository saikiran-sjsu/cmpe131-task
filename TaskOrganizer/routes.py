from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse

from .forms import LoginForm, RegisterForm, TaskForm, ForgotForm
from . import db
from flask import current_app as app
from .models import User, Task


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():

    name = 'Sai'
    title = 'Home'
    form = LoginForm()

    return render_template('home.html', title=title, name=name, form=form)


@app.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))


@app.route('/landing')
@login_required
def landing():
    title = 'Landing Page'
    return render_template('landing.html', title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():

    title = 'Register | Task Organizer'
    form = RegisterForm()
    if form.validate_on_submit():
        users = User(username=form.username.data, email=form.email.data,
                     first_name=form.first_name.data, last_name=form.last_name.data)
        users.set_password(form.password.data)
        users.set_answer(form.question.data)
        db.session.add(users)
        db.session.commit()

        # message = Markup()
        flash('Account Created!' + str(users.first_name))
        # print("Account!")
        return redirect(url_for('login'))
    return render_template('register.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    title = 'Login | Task Organizer'

    print('testing')
    user = User.query.all()

    for u in user:
        print(u.username, u.first_name)

    print('end testing')
    if current_user.is_authenticated:
        return redirect(url_for('landing'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('login')

        return redirect(next_page)

    return render_template('login.html', title=title, form=form)


@app.route('/add', methods=['GET', 'POST'])
def add():

    title = 'Add | Task Organizer'

    tasks = Task.query.all()
    # task = TaskForm(request.form)
    task = TaskForm()
    print('hefasdfasf')
    if task.validate_on_submit():

        tasks = Task(task_name=request.form['task_name'],
                     description=request.form['description'], user_id=current_user.id)
        db.session.add(tasks)
        db.session.commit()

        return redirect(url_for('add'))

    return render_template('add.html', title="add task", form=task, tasks=tasks)


@app.route('/view')
def view():
    title = 'View | Task Organizer'
    tasks = Task.query.filter_by(user_id=current_user.id)

    organize = Task.query.filter_by(user_id=current_user.id).order_by(Task.task_name)

    return render_template('view.html', title=title, tasks=tasks, organize=organize)


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    title = 'Remove | Task Organizer'
    # tasks = Task.query.all()

    tasks = Task.query.filter_by(user_id=current_user.id)
    form = TaskForm()

    if form.validate_on_submit():
        tasks = Task.query.filter_by(task_name=request.form['task_name']).first()
        db.session.delete(tasks)
        db.session.commit()
        return redirect(url_for('remove'))
    return render_template('remove.html', title=title, form=form, tasks=tasks)


@app.route('/delete_all', methods=['POST'])
def delete_all():

    title = 'Remove | Task Organizer'
    Task.query.delete()
    tasks = Task.query.all()
    db.drop_all(tasks)
    db.session.commit()
    tasks = Task.query.all()
    form = TaskForm()
    # if request.form['Yes']:
    #    print('Check here')
#   #     flash('Here')
#
#        return redirect(url_for('remove'))
    return render_template('remove.html', title=title, form=form, tasks=tasks)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():

    title = 'Forgot Password | Task Organizer'

    form = ForgotForm()
    print('hiss')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print('foo')
        if user.check_answer(form.question.data):
            print('moo')
            return redirect(url_for('reset'))

    return render_template('forgot.html', title=title, form=form)


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    title = 'Reset Password | Task Organizer'
    form = ForgotForm()
    print('hi')
    if form.validate_on_submit():
        print('hello')
        user = User.query.filter_by(username=form.username.data).first()
        user.set_password(form.reset_password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset.html', title=title, form=form)
