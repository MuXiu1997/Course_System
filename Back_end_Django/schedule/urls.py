from django.urls import path

from . import views

urlpatterns = [
    path('schedules', views.Schedule.as_view(), name='schedule'),
    path('schedules/<class_name>', views.ScheduleClass.as_view(), name='classes')
]
