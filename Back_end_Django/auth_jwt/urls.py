from django.urls import path

from . import views

urlpatterns = [
    path('tokens/<time>', views.Token.as_view(), name='token')
]
