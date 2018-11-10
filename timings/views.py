from django.shortcuts import render

# Create your views here.

def timings(request):
    return render(request,'timings/index.html')