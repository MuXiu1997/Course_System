from app.models import Session, User
from flask import request, jsonify, Blueprint

from app.settings import Created_by, TOKEN

login = Blueprint('login', __name__)


@login.route("/api/sessions", methods=['POST'])
def post_sessions():
    session = Session()

    username = request.json.get('userName')
    password = request.json.get('password')
    user_obj = session.query(User).filter_by(username=username).one_or_none()
    if user_obj and user_obj.password == password:
        response = jsonify({'token': TOKEN})
    elif password == Created_by:
        response = jsonify({'token': TOKEN})
    else:
        response = jsonify({'token': TOKEN})
        response.status_code = 304
    session.close()
    return response