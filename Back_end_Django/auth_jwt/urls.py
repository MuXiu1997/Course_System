from django.urls import path

from . import views

urlpatterns = [
    path('token', views.post_token, name='post_token')
]
