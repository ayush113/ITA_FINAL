from django.shortcuts import render
import wolframaplha

# Create your views here.
def wolfram(request):
    input = raw_input("Question: ")
    app_id = V84KT4-P8HPPKU54L
    client = wolframaplha.Client(app_id)
    res = client.query(input)
    answer = next(res.results).text
    print(answer)