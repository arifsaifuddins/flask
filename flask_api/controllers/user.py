from flask import jsonify, request
import jwt
from models.auth import User, db
from flask_bcrypt import Bcrypt
from flask import Flask


app = Flask(__name__)
bcrypt = Bcrypt(app)


def registerUser():
  email = request.form['email']
  name = request.form['name']
  password = request.form['password']

  passw = bcrypt.generate_password_hash(password)

  new = User(
      email=email,
      name=name,
      password=passw
  )

  user = User.query.filter_by(email=new.email).first()

  if user is not None:
    return jsonify({
        'status': 401,
        'message': 'User exist'
    }), 401

  db.session.add(new)
  db.session.commit()

  return jsonify({
      'status': 201,
      'message': 'Register Success!',
      'data': {'email': email, 'name': name, 'password': str(passw)}
  }), 201


def loginUser():
  email = request.form['email']
  password = request.form['password']

  user = User.query.filter_by(email=email).first()

  if user is None and not bcrypt.check_password_hash(
          user.password, password):
    return jsonify({
        'status': 401,
        'message': 'password or email incorrect'
    }), 401

  if bcrypt.check_password_hash(user.password, password):
    token = jwt.encode(
        {'email': user.email, 'name': user.name},
        'secretsekali',
        algorithm='HS256'
    )

    emailuser = user.email
    nameuser = user.name

    return jsonify({
        'status': 202,
        'message': 'Login Success!',
        'data': {'email': str(emailuser), 'name': str(nameuser), 'token': str(token)}
    }), 202
