import os
import uuid

from flask import Blueprint, request, Response
from openpyxl import Workbook
from openpyxl.styles import Alignment

from app.models import Major, ClassName, Session
from .schedule import save

xlsx = Blueprint('xlsx', __name__)

align = Alignment(horizontal='center', vertical='center')


@xlsx.route('/xlsx/', methods=['POST'])
def get_xlsx():
    schedules = request.json.get('schedulesData')
    save(schedules)

    work_book = Workbook()  # 创建文件对象
    work_sheet = work_book.active  # 获取第一个sheet
    session = Session()

    def _cell(_row, _col):
        return work_sheet.cell(row=_row, column=_col)

    def put_major():
        index = 2
        for each_major in session.query(Major).filter_by(is_show=True).order_by(Major.order).all():
            _cell(1, index).value = each_major.title
            _cell(1, index).alignment = align
            index += 1

    def put_class():
        index = 2
        for each_class in session.query(ClassName).filter_by(is_show=True).order_by(ClassName.class_name).all():
            work_sheet.merge_cells(start_row=index, start_column=1, end_row=index + 3, end_column=1)
            _cell(index, 1).value = each_class.class_name
            _cell(index, 1).alignment = align
            index += 5

    row_i, col_i = 2, 2
    for row in schedules:
        for col in row['majorInfos']:
            _cell(row_i, col_i).value = '开始时间：{}'.format(col['startDate'][:10] if col['startDate'] else '')
            _cell(row_i + 1, col_i).value = '结束时间：{}'.format(col['endDate'][:10] if col['endDate'] else '')
            _cell(row_i + 2, col_i).value = '周    期：{}'.format(col['duration'])
            _cell(row_i + 3, col_i).value = '讲    师：{}'.format(col['teacher'])
            work_sheet.column_dimensions[_cell(row_i, col_i).column_letter].width = 25
            col_i += 1
        row_i += 5
        col_i = 2

    work_sheet.column_dimensions['A'].width = 12

    put_major()
    put_class()

    session.close()

    file_name = '{}.xlsx'.format(str(uuid.uuid4()))
    work_book.save(file_name)
    with open(file_name, mode='rb') as fp:
        file_r = fp.read()
    os.remove(file_name)

    return Response(response=file_r,
                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
