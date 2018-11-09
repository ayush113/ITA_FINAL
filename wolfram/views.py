from django.shortcuts import render,HttpResponse
import wolframalpha
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_exempt
@login_required
def wolfram(request):
    if request.method =='POST':
        data = request.POST
        term = data.get('term')
        app_id = "V84KT4-P8HPPKU54L"
        client = wolframalpha.Client(app_id)
        res = client.query(term)
        answer = next(res.results).text
        return JsonResponse(answer,safe=False)
    return render(request,'wolfram/index.html')
