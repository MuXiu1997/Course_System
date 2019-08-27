from django.urls import path

from . import views

urlpatterns = [
    path('schedule', views.Schedule, name='schedule'),
    path('schedule/<class_name>', views.ScheduleClass, name='schedule')
]
