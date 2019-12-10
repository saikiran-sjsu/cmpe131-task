from werkzeug.security import generate_password_hash, check_password_hash
from TaskOrganizer import db
from flask_login import UserMixin
from TaskOrganizer import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    question_hash = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    task = db.relationship('Task', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_answer(self, password):
        self.question_hash = generate_password_hash(password)

    def check_answer(self, password):
        return check_password_hash(self.question_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def __repr__(self):
    return '<Task: {} >'.format(self.task_name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
