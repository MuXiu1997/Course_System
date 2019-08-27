import time

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import encode, decode, DecodeError

SECRET = settings.SECRET_KEY


class JWTMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request: HttpRequest):
        if request.path.startswith('/api/tokens'):
            return
        if request.method == 'OPTIONS':
            return
        if request.path.startswith('/admin'):
            return

        token = request.headers.get('Authorization')
        if token is None:
            return http403('缺少认证信息')

        username = check_token(token)
        if username is None:
            return http403('认证失败')


def http403(err):
    return JsonResponse(dict(error=err), status=403)


def create_token(username):
    payload = dict(
        iss='BaiZhi',
        iat=int(time.time()),
        exp=int(time.time()) + 60 * 60 * 24,
        sub=str(username)
    )
    return encode(payload, SECRET).decode()


def check_token(token):
    try:
        payload = decode(token, SECRET)
    except DecodeError:
        return

    iss, iat, exp, sub = payload.get('iss'), payload.get('iat', 0), payload.get('exp', 0), payload.get('sub')

    if not all((iss, iat, exp, sub)):
        return

    try:
        if not iat <= time.time() <= exp:
            return
    except TypeError:
        return

    return sub
