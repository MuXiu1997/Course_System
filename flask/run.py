import json
# import time

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
app.config['SECRET_KEY'] = os.urandom(24)

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(Teacher, Session()))
admin.add_view(ModelView(Major, Session()))
admin.add_view(ModelView(ClassName, Session()))

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
    for each_major in session.query(Major).filter_by(is_show=True).order_by(Major.order).all():
        columns_data.append(
            {
                'title': each_major.title,
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

    for i in table_data:
        for j in i:
            if isinstance(j, dict):
                old_obj = session.query(Archive).filter_by(class_id=i[-1], major_id=j['id']).first()
                if old_obj:
                    session.delete(old_obj)
                    j['startDate'] = j['startDate'][:8] + str((int(j['startDate'][8:10])) + 1) + j['startDate'][10:]
                    j['endDate'] = j['endDate'][:8] + str((int(j['endDate'][8:10]) + 1)) + j['endDate'][10:]
                session.add(Archive(class_id=i[-1],
                                    major_id=j['id'],
                                    info=json.dumps(j, ensure_ascii=False))
                            )
    session.commit()
    session.close()

    return Response(status=200)


@app.route('/api/GET/table-data')
def get_table_data():
    session = Session()

    table_data = []
    for i in session.query(ClassName).filter_by(is_show=True).all():
        a = []
        for j in session.query(Major).filter_by(is_show=True).order_by(Major.order).all():
            c = session.query(Archive).filter_by(class_id=i.id, major_id=j.id).first()
            if c:
                b = json.loads(c.info)
            else:
                b = {
                    'startDate': None,
                    'endDate': None,
                    'duration': j.duration,
                    'teacher': None,
                    'conflictArray': [],
                    'id': j.id
                }
            a.append(b)
        a.append(i.class_name)
        a.append(i.id)
        table_data.append(a)
    return jsonify({'tableData': table_data})


@app.route('/api/POST/new-class', methods=['POST'])
def post_new_class():
    new_class_name = request.json.get('newClassName')

    session = Session()
    new_class_obj = ClassName(class_name=new_class_name)
    session.add(new_class_obj)
    session.commit()

    new_class = []
    for each_major in session.query(Major).filter_by(is_show=True).order_by(Major.order).all():
        new_class.append(
            {
                'startDate': None,
                'endDate': None,
                'duration': each_major.duration,
                'teacher': None,
                'conflictArray': [],
                'id': each_major.id
            },
        )
    new_class.append(new_class_obj.class_name)
    new_class.append(new_class_obj.id)

    session.close()
    return jsonify({'newClass': new_class})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
