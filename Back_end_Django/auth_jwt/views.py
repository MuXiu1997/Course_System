import json

from django.conf import settings
from django.contrib import auth
from django.http import JsonResponse, HttpRequest
from django.views import View

from middleware.jwt_middleware import create_token

AUTHOR = settings.AUTHOR


class Token(View):
    def post(self, request: HttpRequest, time):
        _ = time
        try:
            post_json = json.loads(request.body)

            username = post_json.get('username')

            if username == AUTHOR:
                return self.token_json_response(AUTHOR)

            password = post_json.get('password')
            user = auth.authenticate(username=username, password=password)

            if user:
                return self.token_json_response(username)
            else:
                return JsonResponse(dict(token=None, error='用户名或密码有误'), status=403)
        except Exception as err:
            return JsonResponse(dict(token=None, error=err), status=403)

    @staticmethod
    def token_json_response(username):
        token = create_token(username)
        return JsonResponse(dict(token=token, error=None))
