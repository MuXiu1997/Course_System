import json

from django.http import JsonResponse, HttpRequest
from django.views import View

from .models import Archive, Major, Class


class Schedule(View):
    @staticmethod
    def get(request: HttpRequest):
        return create_schedules_response()

    @staticmethod
    def post(request: HttpRequest):
        try:
            save(*deserialization(request))

            return http200(msg='success', error=None)

        except Exception as err:
            return http400(msg='error', error='请求有误：{}'.format(err))


class ScheduleClass(View):
    @staticmethod
    def post(request: HttpRequest, class_name):
        try:
            new_class = Class.objects.create(name=class_name)
            archives = Archive.objects.filter(class_id=new_class.id)
            [archive.delete() for archive in archives]

            return create_schedules_response()
        except Exception as err:
            return http400(table=None, error=err)


def http200(**kwargs):
    return JsonResponse(kwargs, status=200)


def http400(**kwargs):
    return JsonResponse(kwargs, status=400)


def create_schedules_response():
    try:
        table = create_schedules_data()
        return http200(table=table, error=None)
    except Exception as err:
        return http400(table=None, error=err)


def create_schedules_data():
    headers_and_options = get_model_info_list(Major, is_show=True)
    row_header = get_model_info_list(Class, is_show=True)

    schedules_data = []
    for _class in row_header:
        schedules_data.append(create_class_infos(_class, headers_and_options))

    return dict(
        headersAndOptions=headers_and_options,
        rowHeader=row_header,
        schedulesData=schedules_data,
    )


def deserialization(request: HttpRequest):
    post_json = json.loads(request.body)

    headers_and_options = post_json.get('headersAndOptions')
    row_header = post_json.get('rowHeader')
    schedules_data = post_json.get('schedulesData')
    return headers_and_options, row_header, schedules_data


def save(headers_and_options, row_header, schedules_data):
    for row_index, row in enumerate(schedules_data):
        for col_index, col in enumerate(row):
            archive, _ = Archive.objects.get_or_create(
                class_id=row_header[row_index]['id'],
                major_id=headers_and_options[col_index]['id'],
            )
            archive.info_obj = col
            archive.save()


def create_class_infos(this_class, headers):
    class_infos = []
    for each_major in headers:
        archive, is_create = Archive.objects.get_or_create(class_id=this_class['id'], major_id=each_major['id'])
        if is_create:
            info = {
                'startDate': None,
                'endDate': None,
                'duration': each_major['duration'],
                'teacher': None,
                'conflictArray': [],
            }
        else:
            info = archive.info_obj
        class_infos.append(info)
    return class_infos


def get_model_info_list(model, **kwargs):
    item_list = model.objects.filter(**kwargs).all()
    return [item.info for item in item_list]
