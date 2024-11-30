from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
# Create your views here.
def view_pharm(request):
    return HttpResponse('Hello World')


def home(request):
    return render(request,'home.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                 # https://docs.djangoproject.com/en/5.1/topics/db/queries/
                cust_user = Customer.objects.get(username = username)
            except Customer.DoesNotExist:
                print("Invalid customer username")
                return redirect('login')

            try:
                rep_user = HealthCareRepresentative.objects.get(username = username)
            except HealthCareRepresentative.DoesNotExist:
                print("Invalid rep username")
                return redirect('login')

            try:
                dis_user = Distributer.objects.get(username = username)
            except Distributer.DoesNotExist:
                print("Invalid distributor username")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request,'login.html', {'form':form})

# Reference: https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'signup.html', {'form':form})