from django.urls import re_path

from . import views

urlpatterns = [
    re_path('schedules/(?P<class_name>[^/]+)/?', views.ScheduleClass.as_view(), name='classes'),
    re_path('schedules/?$', views.Schedule.as_view(), name='schedule'),
]
