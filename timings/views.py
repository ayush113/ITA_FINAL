from django.shortcuts import render

from django.db import connection
from notes.utils import namedtuplefetchall
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def timings(request):
    timings = None
    if(request.method == 'POST'):
        data = request.POST
        place = data.get('places')
        with connection.cursor() as curr:
            curr.execute("SELECT open_time,close_time,days_closed from timings where place_name=%s",[place])
            timings = namedtuplefetchall(curr)
    with connection.cursor() as curr:
        curr.execute("Select * from timings")
        res = namedtuplefetchall(curr)
    return render(request,'timings/index.html',{'facilities':res,'timings':timings})