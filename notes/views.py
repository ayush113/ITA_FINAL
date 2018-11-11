from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connection
from .utils import namedtuplefetchall
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.core.mail import send_mail, EmailMessage
import datetime
# Create your views here.
@login_required
@csrf_exempt
def notes(request):
    with connection.cursor() as curr:
        curr.execute("select * from notes where user_id=%s",[request.user.id])
        notes = namedtuplefetchall(curr)
        curr.execute("select id,first_name,last_name from auth_user where not id = %s  ",[request.user.id])
        users = namedtuplefetchall(curr)

    if request.method=='POST':
        data = request.POST
        data = data.get('notes')
        if(data == ''):
            messages.warning(request,message="Empty Note Can not be added")
        else:
            with connection.cursor() as curr:
                curr.execute("INSERT INTO notes(user_id,description) values (%s,%s)",[request.user.id,data])
            return redirect('notes')
    return render(request,'notes/index.html',{'notes':notes,'users':users})

@csrf_exempt
@login_required
def delete(request):
    data = request.POST
    data = data.get('val')
    with connection.cursor() as curr:
        curr.execute("DELETE FROM notes WHERE description=%s and user_id=%s",[data,request.user.id])
    return redirect('notes')


@csrf_exempt
@login_required
def send(request):
    data = request.POST
    content = data.get('content')
    sendto = int(data.get('sendid'))
    from_user = request.user.first_name +" " + request.user.last_name
    if content == '':
        messages.warning(request,message="Can't send empty note")
    else:
        with connection.cursor() as curr:
            curr.execute("Insert into notes values (%s,%s,%s,%s)",[sendto,content,0,from_user])

    return redirect('notes')

@login_required
@csrf_exempt
def backup(request):
    data = request.POST
    print(data)
    with connection.cursor() as curr:
        curr.execute("Select * from notes where user_id=%s",[request.user.id])
        backup = namedtuplefetchall(curr)
    li = []
    for data in backup:
        cont = ''
        cont += 'Description: '
        cont+= data.description
        cont+= '\n'
        li.append(cont)
    data = ''
    for i in li:
        data = data+i
        data += '\n'
    with open('backup.txt','w') as f:
        f.write(data)
    mail = EmailMessage('Backup File','This is your backup file for ' + str(datetime.datetime.now()),to=['gauribaraskar812@gmail.com'])
    file = open('backup.txt')
    mail.attach(file.name,file.read(),'text/text')
    mail.send()
    os.remove('backup.txt')
    messages.info(request,message='Backup Successful')
    return redirect('notes')