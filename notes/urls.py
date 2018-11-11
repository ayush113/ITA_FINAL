from django.urls import path
from . import views


urlpatterns=[
    path('',views.notes,name='notes'),
    path('delete',views.delete,name='deletes'),
    path('send',views.send,name='sends'),
    path('backup',views.backup,name='backup'),
]