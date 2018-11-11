from django.shortcuts import render,redirect
import wolframalpha
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_exempt
@login_required
def wolfram(request):
    answer = None
    term = None
    if request.method =='POST':
        data = request.POST
        term = data.get('term')
        app_id = "V84KT4-P8HPPKU54L"
        client = wolframalpha.Client(app_id)
        res = client.query(term)
        try:
            answer = next(res.results).text
        except:
            messages.warning(request,message="No Results Found")
            return redirect('wolfram')
    return render(request,'wolfram/index.html',{'answer':answer,'term':term})
