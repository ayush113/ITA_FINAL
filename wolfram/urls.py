from django.urls import path
from . import views


urlpatterns=[
    path('',wolfram.views,name='wolfram'),
]