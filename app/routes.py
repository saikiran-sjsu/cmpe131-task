from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from app.forms import LoginForm, RegisterForm, TaskForm, ForgotForm
from app import app


@app.route('/')
@app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)


@app.route('/landing')
@login_required
def landing():
    title = 'Landing Page'
    return render_template('landing.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():

    title = 'Login | Task Organizer'

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
