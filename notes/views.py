from django.shortcuts import render,HttpResponse

from django.db import connection
from .utils import namedtuplefetchall
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def notes(request):
    with connection.cursor() as curr:
        curr.execute("select * from notes where user_id=%s",[request.user.id])
        notes = namedtuplefetchall(curr)
    return render(request,'notes/index.html',{'notes':notes})