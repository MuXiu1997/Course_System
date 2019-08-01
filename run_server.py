from subprocess import call

call(['docker', 'rm', '-f', 'Course_System_flask_uwsgi'])

call(['docker', 'rm', '-f', 'Course_System_nginx'])

call(['docker', 'run', '-d', '-p', '80:80', '--name', 'Course_System_nginx',
      '-v', '/root/Course_System/Front_end_Vue:/app/html',
      '-v', '/root/Course_System/config/nginx.conf:/etc/nginx/nginx.conf',
      '-v', '/root/Course_System/logs:/var/log/nginx',
      'nginx:1.16'])

call(['docker', 'run', '-d', '-it', '-p', '5000:5000', '--name', 'Course_System_flask_uwsgi',
      '-v', '/root/Course_System/Back_end_Flask:/app',
      '-v', '/root/Course_System/config/uwsgi.ini:/app/uwsgi.ini',
      'flask_uwsgi:latest'])
