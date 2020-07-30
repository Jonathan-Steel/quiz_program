# Useful stuff from __init__.py
from quiz_program import db, login_manager

# Used for dates
from datetime import datetime

# A class which provides helpful functions for the login module (such as is_authenticated())
from flask_login import UserMixin

# Allows our login manager to load users by their user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    def __repr__(self):
        return f"Question('{self.term}', '{self.definition}')"

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))

    def __repr__(self):
        return f"Quiz('{self.title}')"

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    quiz = db.relationship('Quiz', backref='chapter', uselist=False)
    textbook_id = db.Column(db.Integer, db.ForeignKey('textbook.id'), nullable=False)

    def __repr__(self):
        return f"Chapter('{self.title}')"

class Textbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    chapters = db.relationship('Chapter', backref='textbook', lazy=True)

    def __repr__(self):
        return f"Textbook('{self.title}')"

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"