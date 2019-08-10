import datetime
import json

from flask import jsonify, Blueprint, request

from app.models import Major, Session, ClassName, Archive

schedule = Blueprint('schedule', __name__)


@schedule.route('/api/schedules')
def get_schedules_data():
    response = create_schedules_data()
    return response


def create_schedules_data():
    session = Session()

    headers_and_options = get_headers_and_options(session)
    row_header = get_row_header(session)

    schedules_data = []
    for _class in row_header:
        schedules_data.append(create_class_infos(_class, headers_and_options, session))
    session.close()

    return jsonify({
        'headersAndOptions': headers_and_options,
        'rowHeader': row_header,
        'schedulesData': schedules_data,
    })


@schedule.route('/api/schedules/<new_class_name>', methods=['POST'])
def post_new_class(new_class_name):

    session = Session()
    new_class_obj = ClassName(class_name=new_class_name)
    session.add(new_class_obj)
    session.commit()
    archives = session.query(Archive).filter_by(class_id=new_class_obj.id)
    [session.delete(archive) for archive in archives]
    session.commit()
    session.close()

    response = create_schedules_data()

    return response


@schedule.route('/api/schedules', methods=['POST'])
def post_table_data():
    headers_and_options = request.json.get('headersAndOptions')
    row_header = request.json.get('rowHeader')
    schedules_data = request.json.get('schedulesData')
    save(headers_and_options, row_header, schedules_data)
    response = jsonify(msg='success')

    return response


def save(headers_and_options, row_header, schedules_data):
    session = Session()

    for row_index, row in enumerate(schedules_data):
        for col_index, col in enumerate(row):
            session.merge(
                Archive(
                    class_id=row_header[row_index]['id'],
                    major_id=headers_and_options[col_index]['id'],
                    info=json.dumps(col, ensure_ascii=False)
                )
            )

    session.commit()
    session.close()


def create_class_infos(this_class, headers, session):
    class_infos = []
    for each_major in headers:
        archive = session.query(Archive).filter_by(class_id=this_class['id'], major_id=each_major['id']).first()
        if archive:
            info = json.loads(archive.info)
        else:
            info = {
                'startDate': None,
                'endDate': None,
                'duration': each_major['duration'],
                'teacher': None,
                'conflictArray': [],
            }
        class_infos.append(info)
    return class_infos


def get_headers_and_options(session):
    """
    获取表头以及对应列的讲师选项
    """
    major_list = session.query(Major).filter_by(is_show=True).order_by(Major.order).all()
    headers_and_options = [major.info for major in major_list]
    return headers_and_options


def get_row_header(session):
    """
    获取每行班级信息
    """
    class_list = session.query(ClassName).filter_by(is_show=True).order_by(ClassName.class_name).all()
    row_header = [_class.info for _class in class_list]
    return row_header
