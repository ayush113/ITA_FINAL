from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import os
import pickle

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def reminds(request):
    return render(request,'reminders/index.html')

@csrf_exempt
def notify(request):
    if os.path.isfile("reminders.pkl"):
        file = open("reminders.pkl","rb")
        res = pickle.load(file)
        li = []
        for row in res:
            print(row)
            if row['user_id'] == request.user.id:
                li.append(row)
        return JsonResponse(li,safe=False)

