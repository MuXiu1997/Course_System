from flask import request, redirect
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from app.models import Teacher, Session, User, Major, ClassName
from app.settings import TOKEN


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        token = request.cookies.get('Token')
        return token == TOKEN

    def inaccessible_callback(self, name, **kwargs):
        response = redirect(request.host_url)
        response.set_cookie('Token', '', 0)
        return response


class MyModelView(ModelView):
    def is_accessible(self):
        token = request.cookies.get('Token')
        return token == TOKEN

    def inaccessible_callback(self, name, **kwargs):
        response = redirect(request.host_url)
        response.set_cookie('Token', '', 0)
        return response


admin = Admin(template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(MyModelView(Teacher, Session()))
admin.add_view(MyModelView(Major, Session()))
admin.add_view(MyModelView(ClassName, Session()))
admin.add_view(MyModelView(User, Session()))
