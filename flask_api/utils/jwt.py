from functools import wraps

from flask import jsonify, make_response, request
import jwt


def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):

    token = request.args.get('api_key') or request.headers.get('key')

    if not token:
      return make_response(jsonify({'message': 'No token found!'}), 404)

    try:
      jwt.decode(token, 'secretsekali', algorithms=['HS256'])
    except BaseException:
      return make_response(jsonify({"message": "Invalid token!"}), 401)

    return f(*args, **kwargs)
  return decorated_function
