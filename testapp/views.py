from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib import messages

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
                invalidCred = False
                 # https://docs.djangoproject.com/en/5.1/topics/db/queries/
                cust_user = Customer.objects.get(username = form_username)   # Syntax: <variable name> = <model name>.objects.get(<dbcolumn=value>)
                print(cust_user.first_name + ' ' + cust_user.last_name) # used for testing

                # https://www.tutorialspoint.com/django/django_sessions.htm
                request.session['username'] = form_username # save the customer username for the home page
                request.session['usertype'] = 1
                return redirect('user') # Redirect to the home site
            
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid username or password')
                print("Invalid customer username")

                # check for representative
                try:
                    # invalidCred = False
                    rep_user = HealthCareRepresentative.objects.get(username = form_username)
                    print(rep_user.first_name + ' ' + rep_user.last_name)
                    request.session['username'] = form_username
                    request.session['usertype'] = 2
                    return redirect('healthrep')
                except HealthCareRepresentative.DoesNotExist:
                    # invalidCred = True
                    print("Invalid rep username")

                    # check for distributer
                    try:
                        dis_user = Distributer.objects.get(username = form_username)
                        request.session['username'] = form_username
                        request.session['usertype'] = 3
                        return redirect('distrib')
                    except Distributer.DoesNotExist:
                        invalidCred = True
                        print("Invalid distributor username")
    else:
        form = LoginForm()

    # if invalidCred:
    #     messages.error(request, "Incorrect Username/Password")

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
    rep = request.session.get('username', default=None)
    repInstance = HealthCareRepresentative.objects.get(username=rep)
    customer_id = None
    cust = Customer.objects.filter(healthcare_rep = rep)
    successString =''
    if request.method == 'POST':
        if 'unlink_customer' in request.POST:
            customer_user = request.POST.get('customer_user')

            try:
                customer_to_unlink = Customer.objects.get(username=customer_user, healthcare_rep=repInstance)
                customer_to_unlink.healthcare_rep = None
                customer_to_unlink.save()
                messages.success(request, "Customer unlinked successfully.")

            except Customer.DoesNotExist:
                messages.error(request, "Customer not found or unauthorized unlink attempt.")
        form = LinkCustForm(request.POST)
        if form.is_valid():
            form_ABID = form.cleaned_data['AB_id']
            form_Fname = form.cleaned_data['Fname']
            form_Lname = form.cleaned_data['Lname']
            try:
                Cust = Customer.objects.get(alberta_healthcare_id=form_ABID, first_name=form_Fname, last_name=form_Lname)
                Cust.healthcare_rep = repInstance
                Cust.save()
                messages.success(request, 'Customer added successfully')
                form = LinkCustForm()
            except Customer.DoesNotExist:
                messages.error(request, "Customer doesn't exist")

    else:
        form = LinkCustForm()

    context = {'logged_in': request.session.get('username', default = None),
               'customers': cust,
               'rep': rep,
               'form': form,
              'customer_id':customer_id
               }

    return render(request, 'healthrep.html', context)