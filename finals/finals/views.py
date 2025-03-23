# from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    # return HttpResponse('Hello MIT113!')
    return render(request, 'index.html')

def about(request):
    # return HttpResponse('MIT113 About page.')
    return render(request, 'about.html')