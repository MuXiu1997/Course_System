import json
import os

from flask import jsonify, Blueprint

workday = Blueprint('workday', __name__)


@workday.route("/api/workdays/")
def get_workday():
    try:
        json_file_name = 'workday_data.json'  # json文件名
        path = os.path.abspath(__file__)  # 当前文件路径
        json_file_path = os.path.join(os.path.dirname(path), json_file_name)  # json文件所在路径
        with open(json_file_path) as file_obj:
            file_obj_r = file_obj.read()
        workday_data = json.loads(file_obj_r)
        response = jsonify({'isWorkdayData': workday_data})

    except Exception as e:
        response = jsonify({'error': str(e)})
        response.status_code = 404
    return response
