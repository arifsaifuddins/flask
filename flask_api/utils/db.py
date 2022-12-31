import os


def connectdb():
  # sql uri
  dirname = os.path.abspath(os.path.dirname(__file__))
  uri = 'sqlite:///' + os.path.join(dirname, 'db.sqlite')
  return uri
