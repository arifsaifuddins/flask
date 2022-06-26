from flask import Flask, flash, make_response, redirect, render_template, url_for, session, request
import os
from sqlalchemy.sql import func

# file upload
from werkzeug.utils import secure_filename
import time

# sql
from flask_sqlalchemy import SQLAlchemy

# cors
from flask_cors import CORS

app = Flask(__name__)
# key for set session
app.secret_key = 'secretkeygenerated'


# sql config
dirname = os.path.abspath(os.path.dirname(__file__))
uri = 'sqlite:///' + os.path.join(dirname, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)


class Student(db.Model):

  # create schema / table
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(80), unique=True)
  age = db.Column(db.Integer)
  created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
  bio = db.Column(db.Text)

  # to inputting
  def __init__(self, firstname, lastname, email, age, bio):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.age = age
    self.bio = bio


# create table
db.create_all()


john = Student(
    firstname='john',
    lastname='doe',
    email='emil@example.com',
    age=23,
    bio='Biology student'
)

aji = Student(
    firstname='aji',
    lastname='saif',
    email='aji@mail.com',
    age=22,
    bio='Islamic student'
)

muhammad = Student(
    firstname='muhammad',
    lastname='saif',
    email='muhammad@mail.com',
    age=22,
    bio='Islamic student'
)

arief = Student(
    firstname='arief',
    lastname='saif',
    email='arief@mail.com',
    age=22,
    bio='Islamic student'
)


# # input row (create)
# db.session.add(john)
# db.session.add(muhammad)
# db.session.commit()


# get all (read)
students = Student.query.all()
for student in students:
  print(student.firstname)


# # get one
# student_one = Student.query.get_or_404(1)
# print(student_one.firstname)


# update (update)
update_std = Student.query.get_or_404(2)
update_std.firstname = 'jamal'
update_std.lastname = 'udin'
update_std.email = 'jamal@mail.com'
update_std.age = 21
update_std.bio = 'kpk'

db.session.add(update_std)
db.session.commit()


# # delete (delete)
# del_std = Student.query.get_or_404(1)

# db.session.delete(del_std)
# db.session.commit()


# basic route
@app.route("/", methods=["GET"])
def root():
  return 'Hello Flask App!'


# jinja template
@app.route('/home', methods=['GET'])
def home_page():
  people = {"name": "arief", "age": "2"}
  admin = ('arief', 'saif', 'udin')
  return render_template("home.jinja", data=(people, admin))


# use params
@app.route("/about/<name>", methods=["GET"])
def about_page(name):

  return render_template(
      'about.jinja', data=f'This is an about page of {name}')


# use query url
@app.route('/contact', methods=['GET'])
def contact_page():
  name = request.args.get('name')
  age = request.args.get('age')

  if not name and not age:
    return render_template('contact.jinja')

  return render_template('contact.jinja', data=(name, age))


# use form
@app.route('/form', methods=['GET', 'POST'])
def form_page():

  if request.method == 'POST':

    email = request.form['email']
    name = request.form['name']

    response = make_response()

    # set cookie ##############
    response.set_cookie('email_cookie', email)

    # set session #############
    session['username'] = request.form['name']

    # set flash message ############ # category
    flash(f'Congrats {name}!, youre logged in as {email}', 'success')

    return redirect(url_for('about_page', name=request.form['name']))

  if 'username' in session:
    name = session['username']

    return redirect(url_for('about_page', name=name))

  return render_template('form.jinja')


# error page handler
@app.errorhandler(404)
def error_page():
  return render_template('404.jinja'), 404


@app.errorhandler(500)
def error_page(e):
  return render_template('500.jinja'), 500


# get cookie
@app.route('/getcookie')
def get_cookie():
  email = request.cookies.get('email_cookie')

  return email


# remove session
@app.route('/logout')
def logout_page():
  session.pop('username', None)

  return redirect(url_for('form_page'))


# uploade file
ALLOWWED_EXT = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'uploads'


def alowwed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWWED_EXT


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':

    file = request.files['file']

    if 'file' not in request.files:
      return redirect(request.url)

    if file.filename == '':
      return redirect(request.url)

    if file and alowwed_file(file.filename):
      tm = str(time.time())
      filename = secure_filename(tm + file.filename)

      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      return 'file save as ' + filename

  return render_template('upload.jinja')


# run server
if __name__ == "__main__":
  app.run(debug=True, port=3002)
