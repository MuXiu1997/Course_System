#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import call
import os

COURSE_SYSTEM = os.path.dirname((os.path.abspath(__file__)))
C_DJANGO = 'Course_System_django'
C_NGINX = 'Course_System_nginx'


def rm():
    call(['docker', 'rm', '-f', C_DJANGO])

    call(['docker', 'rm', '-f', C_NGINX])


def run():
    call(['docker', 'run', '-d', '-p', '80:80', '--name', C_NGINX,
          '-v', os.path.join(COURSE_SYSTEM, 'Front_end_Vue:/app/html'),
          '-v', os.path.join(COURSE_SYSTEM, 'config/nginx.conf:/etc/nginx/nginx.conf'),
          '-v', os.path.join(COURSE_SYSTEM, 'logs:/var/log/nginx'),
          'nginx:1.16-alpine'])

    call(['docker', 'run', '-d', '-p', '5000:5000', '--name', C_DJANGO,
          '-v', os.path.join(COURSE_SYSTEM, 'Back_end_Django:/app'),
          '-v', os.path.join(COURSE_SYSTEM, 'config/uwsgi.ini:/config/uwsgi.ini'),
          'uwsgi_django:latest'])


if __name__ == '__main__':
    c = input('1. 运行容器组\n2. 删除容器组\n')
    if c in (2, '2'):
        rm()
    else:
        rm()
        run()
