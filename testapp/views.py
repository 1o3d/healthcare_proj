from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
# Create your views here.
def view_pharm(request):
    return HttpResponse('Hello World')


def home(request):
    # https://www.tutorialspoint.com/django/django_sessions.htm
    return render(request,'home.html',{'logged_in': request.session.get('username', default = None)}) # send a username forwards to the home page render (Can be None)

# Login mechanics
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_username = form.cleaned_data['username']
            form_password = form.cleaned_data['password']

            # check for customer first
            try:
                 # https://docs.djangoproject.com/en/5.1/topics/db/queries/
                cust_user = Customer.objects.get(username = form_username)   # Syntax: <variable name> = <model name>.objects.get(<dbcolumn=value>)
                print(cust_user.first_name + ' ' + cust_user.last_name) # used for testing

                # https://www.tutorialspoint.com/django/django_sessions.htm
                request.session['username'] = form_username # save the customer username for the home page
                request.session['usertype'] = 1
                return redirect('user') # Redirect to the home site
            
            except Customer.DoesNotExist:
                print("Invalid customer username")

                # check for representative
                try:
                    rep_user = HealthCareRepresentative.objects.get(username = form_username)
                    print(rep_user.first_name + ' ' + rep_user.last_name)
                    request.session['username'] = form_username
                    request.session['usertype'] = 2
                    return redirect('healthrep')
                except HealthCareRepresentative.DoesNotExist:
                    print("Invalid rep username")

                    # check for distributer
                    try:
                        dis_user = Distributer.objects.get(username = form_username)
                        request.session['username'] = form_username
                        request.session['usertype'] = 3
                        return redirect('distrib')
                    except Distributer.DoesNotExist:
                        print("Invalid distributor username")
    else:
        form = LoginForm()
    return render(request,'login.html', {'form':form})

# A simple log out request. Reference: https://www.tutorialspoint.com/django/django_sessions.htm
def logging_out(request):
    del request.session['username'] # delete the sessions cookies
    return redirect('home') # redirect to the main page

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

def user(request):
    return render(request, 'user.html',{'logged_in': request.session.get('username', default = None)})

def distrib(request):
    return render(request, 'distrib.html',{'logged_in': request.session.get('username', default = None), 'user_type': request.session.get('usertype', default=0)})

def healthrep(request):
    return render(request, 'healthrep.html',{'logged_in': request.session.get('username', default = None)})