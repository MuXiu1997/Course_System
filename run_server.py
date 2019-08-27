# -*- coding: utf-8 -*-
from subprocess import call

COURSE_SYSTEM = '/root/Course_System_v20190827/'
C_DJANGO = 'Course_System_django_v20190827'
C_NGINX = 'Course_System_nginx_v20190827'


def rm():
    call(['docker', 'rm', '-f', C_DJANGO])

    call(['docker', 'rm', '-f', C_NGINX])


def run():
    call(['docker', 'run', '-d', '-p', '80:80', '--name', C_NGINX,
          '-v', COURSE_SYSTEM + 'Front_end_Vue:/app/html',
          '-v', COURSE_SYSTEM + 'config/nginx.conf:/etc/nginx/nginx.conf',
          '-v', COURSE_SYSTEM + 'logs:/var/log/nginx',
          'nginx:1.16'])

    call(['docker', 'run', '-d', '-p', '5000:5000', '--name', C_DJANGO,
          '-v', COURSE_SYSTEM + 'Back_end_Django:/app',
          '-v', COURSE_SYSTEM + 'config/uwsgi.ini:/app/uwsgi.ini',
          'uwsgi_django:latest'])


if __name__ == '__main__':
    c = input('1. 运行容器组\n2. 删除容器组\n')
    if c in (2, '2'):
        rm()
    else:
        rm()
        run()
