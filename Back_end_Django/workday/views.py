import json
import os

from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.views import View

JSON_FILE_NAME = 'workday_data.json'
BASE_DIR = settings.BASE_DIR


class Workday(View):
    def get(self, request: HttpRequest):
        _ = request
        try:
            with open(self.json_file_path) as fp:
                content = fp.read()
            workday_data = json.loads(content)
            return JsonResponse(dict(isWorkdayData=workday_data, error=None))
        except FileNotFoundError as err:
            return JsonResponse(dict(isWorkdayData=None, error=err), status=404)

    @property
    def json_file_path(self):
        return os.path.join(BASE_DIR, JSON_FILE_NAME)
