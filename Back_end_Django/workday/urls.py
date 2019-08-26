from django.urls import path

from . import views

urlpatterns = [
    path('workdays', views.get_workdays, name='get_workdays')
]
