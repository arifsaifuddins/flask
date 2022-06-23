from flask import Flask, flash, make_response, redirect, render_template, url_for, session, request
import os

# file upload
from werkzeug.utils import secure_filename
import time

# sql
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# key for set session
app.secret_key = 'secretkeygenerated'


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

  return render_template('about.jinja', data=f'This is an about page of {name}')


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
