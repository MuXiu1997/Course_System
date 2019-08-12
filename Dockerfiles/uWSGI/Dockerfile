FROM python:3.7.3

RUN pip install flask -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

RUN pip install flask-cors -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

RUN pip install flask-admin -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

RUN pip install openpyxl -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

RUN pip install requests -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

RUN pip install uwsgi -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

RUN pip install sqlalchemy -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

RUN pip install pyjwt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

COPY ./uwsgi.ini /app/uwsgi.ini

EXPOSE 5000

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
