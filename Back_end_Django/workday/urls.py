from django.urls import path

from . import views

urlpatterns = [
    path('workdays', views.Workday.as_view(), name='workday')
]
