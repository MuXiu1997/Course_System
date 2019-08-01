import datetime
import json

from flask import jsonify, Blueprint, request

from app.models import Major, Session, ClassName, Archive

schedule = Blueprint('schedule', __name__)


@schedule.route('/api/schedules')
def get_table_data():
    session = Session()

    schedules_data = []
    for each_class in session.query(ClassName).filter_by(is_show=True).order_by(ClassName.class_name).all():
        schedules_data.append(create_class_infos(each_class, session))
    session.close()
    columns_data = get_columns_options_data()
    return jsonify({
        'schedulesData': schedules_data,
        'columnsData': columns_data,
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

    new_class = create_class_infos(new_class_obj, session)

    session.close()
    return jsonify({'newClass': new_class})


@schedule.route('/api/schedules', methods=['POST'])
def post_table_data():
    schedules = request.json.get('schedulesData')
    save(schedules)
    response = jsonify(msg='success')

    return response


def save(schedules):
    session = Session()

    for each_row in schedules:
        for each_col in each_row['majorInfos']:
            each_col['startDate'] = get_correct_date(each_col['startDate']) if each_col['startDate'] else ''
            each_col['endDate'] = get_correct_date(each_col['endDate']) if each_col['endDate'] else ''
            session.merge(
                Archive(
                    class_id=each_row['classID'],
                    major_id=each_col['id'],
                    info=json.dumps(each_col, ensure_ascii=False)
                )
            )

    session.commit()
    session.close()


def create_class_infos(this_class, session):
    class_infos = {
        'classID': this_class.id,
        'className': this_class.class_name,
        'majorInfos': []
    }
    for each_major in session.query(Major).filter_by(is_show=True).order_by(Major.order).all():
        archive = session.query(Archive).filter_by(class_id=this_class.id, major_id=each_major.id).first()
        if archive:
            info = json.loads(archive.info)
        else:
            info = {
                'startDate': None,
                'endDate': None,
                'duration': each_major.duration,
                'teacher': None,
                'conflictArray': [],
                'id': each_major.id
            }
        class_infos['majorInfos'].append(info)
    return class_infos


def get_columns_options_data():
    """
    获取表头以及对应列的讲师选项
    """
    session = Session()
    columns_data = [
        {
            'title': major.title,
            'options': [teacher.name for teacher in major.teacher]
        } for major in session.query(Major).filter_by(is_show=True).order_by(Major.order).all()
    ]
    session.close()
    return columns_data


def get_correct_date(date_str):
    correct_date = datetime.date(
        int(date_str[:4]),
        int(date_str[5:7]),
        int(date_str[8:10])
    ) + datetime.timedelta(1)

    return str(correct_date) + date_str[10:]
