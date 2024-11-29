from django.shortcuts import render
from django.http import HttpResponse
from . import forms

# Create your views here.
def view_pharm(request):
    return HttpResponse('Hello World')


def home(request):
    return render(request,'home.html')


def login(request):
    form = forms.CustomerForm
    return render(request,'login.html', {'form':form})