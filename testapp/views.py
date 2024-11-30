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

            # check for customer first
            try:
                 # https://docs.djangoproject.com/en/5.1/topics/db/queries/
                cust_user = Customer.objects.get(username = username)   # Syntax: <variable name> = <model name>.objects.get(<dbcolumn=value>)
                print(cust_user.first_name + ' ' + cust_user.last_name)
            except Customer.DoesNotExist:
                print("Invalid customer username")

                # check for representative
                try:
                    rep_user = HealthCareRepresentative.objects.get(username = username)
                    print(rep_user.first_name + ' ' + rep_user.last_name)
                except HealthCareRepresentative.DoesNotExist:
                    print("Invalid rep username")

                    # check for distributer
                    try:
                        dis_user = Distributer.objects.get(username = username)
                    except Distributer.DoesNotExist:
                        print("Invalid distributor username")
    else:
        form = LoginForm()
    return render(request,'login.html', {'form':form})

# Reference: https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request,'signup.html', {'form':form})