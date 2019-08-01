from os import urandom

from flask import Flask
from flask_cors import CORS

from .admin import admin
from .api import login, workday, schedule, xlsx


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = urandom(24)
    CORS(app, resources={r"/api/*|/xlsx": {"origins": "*"}})  # 使前端能从后端拿到数据
    admin.init_app(app)

    app.register_blueprint(login)
    app.register_blueprint(workday)
    app.register_blueprint(schedule)
    app.register_blueprint(xlsx)

    return app
