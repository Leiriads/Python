from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def registration(request):
    return render(request,'cadastro.html')

def login(request):
    return HttpResponse("Você está na página de login") 