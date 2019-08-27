from django.urls import re_path

from . import views

urlpatterns = [
    re_path('tokens/(?P<time>.*?)/?', views.Token.as_view(), name='token')
]
