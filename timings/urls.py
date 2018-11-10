from django.urls import path

from . import views

urlpatterns=[
    path('',views.timings,name='timings')
]