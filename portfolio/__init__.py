""" Creates the app, creates the database, and initializes the expletives """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from portfolio import models
db.drop_all()
db.create_all()
censor = {"fuck": "f***", "shit": "s***", "crap": "c***", "damn": "d***", "bitch": "b****", "ass": "a**"}
for word in censor:
    new_expletive = models.Expletives(word, censor[word])
    db.session.add(new_expletive)
    db.session.commit()
from portfolio import views
