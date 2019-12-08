from flask import render_template, redirect, url_for
from app import app

@app.route('/')
@app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)

