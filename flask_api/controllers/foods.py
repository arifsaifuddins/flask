from flask import jsonify, request
from models.foods import Student, db


def addStudent():
  email = request.form['email']
  name = request.form['name']
  poster = request.form['poster']

  new = Student(
      email=email,
      name=name,
      poster=poster
  )

  student = Student.query.filter_by(email=new.email).first()

  if student is not None:
    return jsonify({
        'status': 401,
        'message': 'error'
    }), 401

  db.session.add(new)
  db.session.commit()

  return jsonify({
      'status': 201,
      'message': 'Add Success!',
      'data': [email, name, poster]
  }), 201


def getStudent():
  students = Student.query.all()
  student = {}

  for std in students:
    student.copy()
    student[std.id] = {
        'email': std.email,
        'name': std.name,
        'poster': std.poster
    }

  return jsonify({
      'status': 200,
      'message': 'Get Success!',
      'data': student
  }), 200


def delStudent(id):
  student = Student.query.get(id)

  if student:
    db.session.delete(student)
    db.session.commit()

    return jsonify({
        'status': 202,
        'message': f'{student.name} deleted'
    }), 202

  return jsonify({
      'status': 404,
      'message': 'Student not Found'
  }), 404


def updateStudent(id):
  student = Student.query.get(id)

  if student:
    student.email = request.form.get('email') or student.email
    student.name = request.form.get('name') or student.name
    student.poster = request.form.get('poster') or student.poster

    db.session.add(student)
    db.session.commit()

    return jsonify({
        'status': 202,
        'message': f'{student.name} updated',
        'data': {
            'email': student.email,
            'name': student.name,
            'poster': student.poster,
        }
    }), 202

  return jsonify({
      'status': 404,
      'message': 'Student not Found'
  }), 404
