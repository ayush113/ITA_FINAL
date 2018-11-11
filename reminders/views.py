from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import os
import pickle
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from notes.utils import namedtuplefetchall

# Create your views here.
@csrf_exempt
@login_required
def reminds(request):
    if request.method == 'POST':
        data = request.POST
        desc = data.get('desc')
        time = data.get('rtime')
        li = time.split('T')
        print(li)
        val = li[0]+' '+li[1]+':00'

        with connection.cursor() as curr:
            curr.execute("INSERT INTO reminders VALUES(%s,%s,%s)",[request.user.id,desc,val])
        return JsonResponse(1,safe=False)
    else:
        with connection.cursor() as curr:
            curr.execute("SELECT * FROM reminders WHERE user_id=%s",[request.user.id])
            reminders = namedtuplefetchall(curr)
        number = len(reminders)
        return render(request,'reminders/index.html',{'reminders':reminders,'number':number})

@csrf_exempt
def removes(request):
    data = request.POST
    desc = data.get('desc')
    uid = request.user.id
    with connection.cursor() as curr:
        curr.execute("DELETE FROM reminders WHERE description=%s AND user_id=%s",[desc,uid])
    return JsonResponse(1,safe=False)

@csrf_exempt
def notify(request):
    if os.path.isfile("reminders.pkl"):
        file = open("reminders.pkl","rb")
        res = pickle.load(file)
        print(res)
        li = []
        for row in res:
            if row['user_id'] == request.user.id:
                li.append(row)
        if len(li) == 0:
            row = {'nores':1}
            li.append(row)
        return JsonResponse(li,safe=False)

