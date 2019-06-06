import datetime
import json
import logging

import requests
from flask import Flask, jsonify, Response, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS

from models import *

from openpyxl import Workbook
from openpyxl.styles import Alignment

# import time

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
    return columns_data


def get_options_data():
    session = Session()
    options_data = []

    for each_major in session.query(Major).filter_by(is_show=True).order_by(Major.order).all():
        names = []
        for teacher in each_major.teacher:
            names.append(teacher.name)
        options_data.append(names)

    session.close()
    return options_data


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

    return jsonify({'tableData': table_data,
                    'optionsData': get_options_data(),
                    'columnsData': get_columns_data()
                    })


@app.route('/api/POST/table-data', methods=['POST'])
def post_table_data():
    def get_correct_date(date_str):
        correct_date = datetime.date(
            int(date_str[:4]),
            int(date_str[5:7]),
            int(date_str[8:10])
        ) + datetime.timedelta(1)

        return str(correct_date) + date_str[10:]

    session = Session()

    table_data = request.json.get('tableData')

    for i in table_data:
        for j in i:
            if isinstance(j, dict):
                old_obj = session.query(Archive).filter_by(class_id=i[-1], major_id=j['id']).first()
                if old_obj:
                    session.delete(old_obj)
                    j['startDate'] = get_correct_date(j['startDate'])
                    j['endDate'] = get_correct_date(j['endDate'])

                session.add(
                    Archive(
                        class_id=i[-1],
                        major_id=j['id'],
                        info=json.dumps(j, ensure_ascii=False)
                    )
                )

    if 1:
        wb = Workbook()  # 创建文件对象
        ws = wb.active  # 获取第一个sheet
        align = Alignment(horizontal='center', vertical='center')

        def _cell(row, col, ws=ws):
            return ws.cell(row=row, column=col)

        def put_major():
            i_ = 2
            for each_major in session.query(Major).filter_by(is_show=True).order_by(Major.order).all():
                _cell(1, i_).value = each_major.title
                _cell(1, i_).alignment = align
                i_ += 1

        def put_class():
            i_ = 2
            for each_class in session.query(ClassName).filter_by(is_show=True).all():
                ws.merge_cells(start_row=i_, start_column=1, end_row=i_ + 3, end_column=1)
                _cell(i_, 1).value = each_class.class_name
                _cell(i_, 1).alignment = align
                i_ += 5

        row_i, col_i = 2, 2
        for i in table_data:
            for j in i:
                if isinstance(j, dict):
                    _cell(row_i, col_i).value = '开始时间：%s' % get_correct_date(j['startDate'])[:10]
                    _cell(row_i + 1, col_i).value = '结束时间：%s' % get_correct_date(j['endDate'])[:10]
                    _cell(row_i + 2, col_i).value = '周    期：%s' % j['duration']
                    _cell(row_i + 3, col_i).value = '讲    师：%s' % j['teacher']
                    ws.column_dimensions[_cell(row_i, col_i).column_letter].width = 25
                col_i += 1
            row_i += 5
            col_i = 2

        ws.column_dimensions['A'].width = 12

        put_major()
        put_class()
        wb.save('a.xlsx')

    session.commit()
    session.close()

    return Response(response=open('a.xlsx', mode='rb'), status=200,
                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


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
