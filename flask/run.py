import json
import time

from flask import Flask, jsonify, Response, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
import requests

from models import *
import logging

logging.basicConfig(level=logging.DEBUG)

HUA_JI = False

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  # 使前端能从后端拿到数据

admin = Admin(app)
admin.add_view(ModelView(Teacher, Session()))
admin.add_view(ModelView(Major, Session()))

HOST = '0.0.0.0'
PORT = 5000


@app.route("/api/GET/workday-data")
def get_workday_data():
    """
    是否工作日的api
    """
    year = request.args.get("year", "2019")
    filename = year + 'workday_data.json'
    workday_data = dict()

    try:
        with open(filename) as file_obj:
            workday_data = json.load(file_obj)

    except FileNotFoundError:
        if not workday_data:
            url = 'http://www.mxnzp.com/api/holiday/list/year/' + year
            request_api_text = requests.get(url).text
            request_api_json = json.loads(request_api_text)
            for each_month in request_api_json['data']:
                for each_day in each_month['days']:
                    workday_data[each_day['date']] = each_day['typeDes'] == '工作日'
            with open(filename, 'w', encoding='utf8') as api_file_obj:
                json.dump(workday_data, api_file_obj, ensure_ascii=False)

    return jsonify({'isWorkdayData': workday_data})


@app.route('/api/GET/columns-data')
def get_columns_data():
    session = Session()
    columns_data = []
    for each_major in session.query(Major).all():
        columns_data.append(
            {
                'title': each_major.title,
                'width': 310,
                'slot': each_major.id
            }
        )
    session.close()
    return jsonify({'columnsData': columns_data})


@app.route('/api/GET/options-data')
def get_options_data():
    session = Session()
    options_data = []

    for each_major in session.query(Major).all():
        names = []
        for teacher in each_major.teacher:
            names.append(teacher.name)
        options_data.append(names)

    session.close()
    return jsonify({'optionsData': options_data})


@app.route('/api/GET/duration-data')
def get_duration_data():
    session = Session()
    duration_data = []

    for each_major in session.query(Major).all():
        duration_data.append(each_major.duration)

    session.close()
    return jsonify({'optionsData': duration_data})


@app.route('/api/POST/table-data', methods=['POST'])
def post_table_data():
    session = Session()

    table_data = request.json.get('tableData')
    #
    # for index in range(len(table_data)):
    #     del table_data[index]["_index"]
    #     del table_data[index]["_rowKey"]
        # class_name = table_data[index]["className"]
        # del table_data[index]["className"]
        # table_data[index] = dict({'className': class_name}, **table_data[index])

    table_data_obj = Archive(time=time.time(), info=json.dumps(table_data, ensure_ascii=False))
    session.add(table_data_obj)

    session.commit()
    session.close()
    return Response(status=200)


@app.route('/api/GET/table-data')
def get_table_data():
    session = Session()

    _time = request.args.get("time")
    print(_time)
    table_data = ''
    if _time:
        pass
    else:
        table_data_obj = session.query(Archive).all()[-1]
        table_data = json.loads(table_data_obj.info)

    session.close()
    return jsonify({'tableData': table_data})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
