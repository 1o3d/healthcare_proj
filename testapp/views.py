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
    if request.method == 'POST':
        form1 = forms.CustomerForm(request.POST)
        if(form1.is_valid()):
            form1.save()
            return HttpResponse('Succesfully apressed submit and maybe added to database?')
    return render(request,'login.html', {'form':form})