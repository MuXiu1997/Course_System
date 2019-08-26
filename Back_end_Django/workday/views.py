import json
import os

from django.conf import settings
from django.http import JsonResponse, HttpRequest

JSON_FILE_NAME = 'workday_data.json'
BASE_DIR = settings.BASE_DIR


def get_workdays(request: HttpRequest):
    try:
        json_file_path = os.path.join(BASE_DIR, JSON_FILE_NAME)
        with open(json_file_path) as fp:
            content = fp.read()
        workday_data = json.loads(content)
        return JsonResponse(dict(isWorkdayData=workday_data, error=None))
    except FileNotFoundError as err:
        return JsonResponse(dict(isWorkdayData=None, error=err), status=404)