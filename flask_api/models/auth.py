from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from sqlalchemy.sql import func


from utils.db import connectdb


app = Flask(__name__)


# sql config
app.config['SQLALCHEMY_DATABASE_URI'] = connectdb()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class User(db.Model):

  # create schema / table
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  name = db.Column(db.String(100))
  password = db.Column(db.String(100))
  created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

  # to inputting
  def __init__(self, email, name, password):
    self.email = email
    self.name = name
    self.password = password


# create table
with app.app_context():
  db.create_all()
# db.drop_all()
