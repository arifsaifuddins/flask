import os
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from controllers.foods import addStudent, delStudent, getStudent, updateStudent
from controllers.user import loginUser, registerUser
from models import foods, auth


from utils.db import connectdb
from utils.jwt import login_required


app = Flask(__name__)


# sql config
app.config['SQLALCHEMY_DATABASE_URI'] = connectdb()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


CORS(app)


@app.errorhandler(404)
def error(e):
  return jsonify({
      'status': 404,
      'message': str(e).split(':')[0]
  })


@app.route('/404')
def do():
  return render_template('404.jinja')


@app.route('/')
def welcome():
  b_data = bcrypt.generate_password_hash('Welcome to API')
  data = bcrypt.check_password_hash(b_data, 'Welcome to API')

  return jsonify({
      'status': 200,
      'message': str(b_data),
      'is-true': data
  })


@app.post('/register')
def signup():
  return registerUser()


@app.post('/login')
def signin():
  return loginUser()


@app.post('/add-student')
def add():
  if request.method == 'POST':
    return addStudent()


@app.get('/get-student')
@login_required
def get():
  return getStudent()


@app.delete('/del-student/<id>')
def delete(id):
  return delStudent(id)


@app.put('/put-student/<id>')
def update(id):
  return updateStudent(id)


# port
if __name__ == '__main__':
  app.run(debug=True, port=2003, host='0.0.0.0')
