from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def view_pharm(request):
    return HttpResponse('Hello World')


def home(request):
    return render(request,'home.html')


def login(request):
    return render(request,'login.html')