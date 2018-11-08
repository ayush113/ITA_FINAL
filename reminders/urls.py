from django.urls import path

from . import views

urlpatterns = [
    path('',views.reminds,name='remind'),
    path('notify',views.notify,name='notification'),
]