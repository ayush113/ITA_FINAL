from django.shortcuts import render,HttpResponse
import wolframalpha

# Create your views here.
def wolfram(request):
    input = "hi meaning"
    app_id = "V84KT4-P8HPPKU54L"
    client = wolframalpha.Client(app_id)
    res = client.query(input)
    answer = next(res.results).text
    print(answer)
    return HttpResponse(answer)
