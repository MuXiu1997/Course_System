FROM python:3.7.3

RUN pip install uwsgi -i http://pypi.douban.com/simple --trusted-host pypi.douban.com \
&& pip install django -i http://pypi.douban.com/simple --trusted-host pypi.douban.com \
&& pip install pyjwt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com \
&& pip install openpyxl -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

COPY ./uwsgi.ini /app/uwsgi.ini

EXPOSE 5000

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
