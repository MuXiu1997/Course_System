from django.urls import path

from . import views

urlpatterns = [
    path('', views.XLSX.as_view(), name='xlsx')
]
