import json

from flask import jsonify, Blueprint

workday = Blueprint('workday', __name__)


@workday.route("/api/workdays")
def get_workday():
    try:
        # 最终会在与 manage.py 同级目录中
        with open('workday_data.json') as file_obj:
            file_obj_r = file_obj.read()
        workday_data = json.loads(file_obj_r)
        response = jsonify({'isWorkdayData': workday_data})

    except Exception as e:
        response = jsonify({'error': str(e)})
        response.status_code = 404
    return response
