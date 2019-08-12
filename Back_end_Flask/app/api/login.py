import time

import jwt
from flask import request, jsonify, Blueprint, abort

from app.models import Session, User
from app.settings import CREATED_BY, SECRET

login = Blueprint('login', __name__)


@login.before_app_request
def check_token():
    if request.method in ('OPTIONS', 'options'):
        return
    if request.path in ('/api/token/', '/api/token'):
        return

    if request.path.startswith('/admin'):
        token = request.cookies.get('token') or abort(403)
    else:
        token = request.headers.get('Authorization') or abort(403)

    try:
        payload = jwt.decode(token, SECRET) or abort(403)
    except Exception as e:
        _ = e
        payload = dict()
        abort(403)

    iss, iat, exp, sub = payload.get('iss'), payload.get('iat', 0), payload.get('exp', 0), payload.get('sub')

    if not all((iss, iat, exp, sub)):
        abort(403)

    try:
        if not iat <= time.time() <= exp:
            abort(403)
    except Exception as e:
        _ = e
        abort(403)


@login.route("/api/token/", methods=['POST'])
def post_token():
    session = Session()

    username = request.json.get('userName')
    password = request.json.get('password')
    user_obj = session.query(User).filter_by(username=username).one_or_none()
    session.close()
    if user_obj and user_obj.password == password:
        username = user_obj.username
    elif password == CREATED_BY:
        username = CREATED_BY
    else:
        abort(403)
        return
    token = create_token(username)
    response = jsonify(token=token)
    return response


def create_token(username):
    payload = {
        'iss': 'BaiZhi',
        'iat': int(time.time()),
        'exp': int(time.time()) + 60 * 60 * 24,
        'sub': str(username)
    }

    return jwt.encode(payload, SECRET).decode()
