from django.urls import path
from . import views


urlpatterns=[
    path('',views.wolfram,name='wolfram'),
]