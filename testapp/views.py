from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *
from django.db.models import Subquery
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
                        dist_user = Distributer.objects.get(username = form_username)
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
    request.session.flush() # delete the sessions cookies
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
    cust_id = Customer.objects.get(username = request.session['username'])
    ingredients = Ingredient.objects.all()
    allergies = Allergy.objects.filter(cust_healthcare_id=cust_id)
    prescriptions = Prescription.objects.filter(cust_healthcare_id=cust_id)
    insurance = InsurancePlan.objects.filter(cust_healthcare_id=cust_id)
    coverages = InsuranceCoverage.objects.filter(cust_healthcare_id=cust_id)
    matching_prescs = Prescription.objects.filter(
        cust_healthcare_id=cust_id
    ).values('prescription_name')
    presc_meds = Medication.objects.filter(
        med_name__in=Subquery(matching_prescs)
    )

    returnstruct = {
        'logged_in': request.session.get('username', default = None),
        'ingredients': ingredients,
        'allergies': allergies,
        'prescriptions': prescriptions,
        'plans': insurance,
        'covs': coverages,
        'meds': presc_meds
    }
    return render(request, 'user.html',returnstruct)

def user_create_allergy(request):
    cust_id = Customer.objects.get(username = request.session['username'])
    if request.method == "POST":
        symptoms_text = request.POST.get('sympinp')
        ingredients_input_id = request.POST.get('ingrinput')
        print("symptoms_text = " + symptoms_text)
        print("ingredients_input_id = " + ingredients_input_id)
        if symptoms_text and ingredients_input_id:
            ingredients_id = Ingredient.objects.get(iupac_name=ingredients_input_id)
            Allergy.objects.create(symptoms=symptoms_text,cust_healthcare_id=cust_id,ingredient_id=ingredients_id)
    return redirect('user')

def user_delete_allergy(request):
    if request.method == "POST":
        todelete = request.POST.get('delbutton')
        print("deleting " + todelete)
        Allergy.objects.filter(pk=todelete).delete()
    return redirect('user')

def user_create_pres(request):
    cust_id = Customer.objects.get(username = request.session['username'])
    if request.method == "POST":
        pname = request.POST.get('presnameinput')
        pdosage = request.POST.get('presamountinput')
        refdate = request.POST.get('presrefilldate')
        rxnum = request.POST.get('presrxinput')
        print("pname = " + pname)
        print("dosage = " + pdosage)
        if pname and pdosage and refdate:
            Prescription.objects.create(cust_healthcare_id=cust_id,prescription_name=pname,refill_date=refdate,dosage=pdosage,rx_number=rxnum)
    return redirect('user')

def user_delete_pres(request):
    if request.method == "POST":
        todelete = request.POST.get('presdelbutton')
        print("deleting " + todelete)
        Prescription.objects.filter(rx_number=todelete).delete()
    return redirect('user')

def user_create_insurance(request):
    cust_id = Customer.objects.get(username = request.session['username'])
    if request.method == "POST":
        coveragetype = request.POST.get('insurancetypeinput')
        if coveragetype:
            InsurancePlan.objects.create(coverage_type=coveragetype,cust_healthcare_id=cust_id)
    return redirect('user')

def user_delete_insurance(request):
    if request.method == "POST":
        todelete = request.POST.get('plandelbutton')
        InsurancePlan.objects.filter(health_insurance_field=todelete).delete()
    return redirect('user')

def user_create_coverage(request):
    cust_id = Customer.objects.get(username = request.session['username'])
    if request.method == "POST":
        insplan = InsurancePlan.objects.get(health_insurance_field=request.POST.get('insselect'))
        rxnum = Prescription.objects.get(rx_number=request.POST.get('covpres'))
        covamt = request.POST.get('covperc')

        if insplan and rxnum and covamt:
            InsuranceCoverage.objects.create(health_insurance_field=insplan,rx_number=rxnum,coverage_amount=covamt,cust_healthcare_id=cust_id)
    return redirect('user')

def user_delete_coverage(request):
    return

def distrib(request):
    # grab the distributer data
    dist_user = Distributer.objects.get(username = request.session['username'])
    # grab the medications associated with that distributer
    dist_medications = Medication.objects.filter(distributer_id = dist_user.distributer_id)
    # grab every inventory that stores medication that this distributor has supplied.
    dist_inventories = Inventory.objects.filter(distributer_id = dist_user.distributer_id)
    # medication ingrediants
    med_ingredients = MedicationIngredients.objects.filter(med_name__in = dist_medications).values('med_name','iupac_name')

    # filter medication ingredients further using a get request:
    #selected_med = request.GET.get('medication')
    #print(f"Selected Medication: {selected_med}")

    if request.method == 'POST':
        med_form = MedForm(request.POST)
        ing_form = IngredientForm(request.POST)
        med_ing_form = MedicationIngredientForm(request.POST)
        if med_form.is_valid():
            # https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/#:~:text=If%20you%20call%20save(),on%20the%20resulting%20model%20instance.
            # The form is created but not saved, we still need to input the dist id attribute
            medication = med_form.save(commit=False)
            # Although it's a foreign key of type CHAR. This is actually asking for a distributer to be assigned to.
            medication.distributer_id = dist_user
            medication.save() #Add the medication
        elif ing_form.is_valid():
            ing_form.save()

        elif med_ing_form.is_valid():
            medication_ingredient = med_ing_form.save(commit=False)
            medication_ingredient.distributer_id = dist_user
            medication_ingredient.save()
    else:
        med_form = MedForm()
        ing_form = IngredientForm()
        med_ing_form = MedicationIngredientForm()
    # send over the re;evant medications for render
    return render(request,'distrib.html',
        {
            'logged_in': request.session.get('username', default = None), 
            'meds':dist_medications,
            'add_med_form':med_form,
            'add_ing_form':ing_form,
            'add_med_ing_form':med_ing_form,
            'inventories':dist_inventories,
            'med_ingredients':list(med_ingredients)
        })


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

def customer_details(request, customer_username):
    custHealthID = Customer.objects.get(username=customer_username).alberta_healthcare_id
    customer = get_object_or_404(Customer, username=customer_username)

    try:
        custPhone = CustomerPhone.objects.get(alberta_healthcare_id=custHealthID).cust_phone_field
    except CustomerPhone.DoesNotExist:
        custPhone = "No phone number provided"

    try:
        custEmail = CustomerEmail.objects.get(alberta_healthcare_id=custHealthID).cust_email
    except CustomerEmail.DoesNotExist:
        custEmail = "No email provided"

    allergies = Allergy.objects.filter(cust_healthcare_id=custHealthID).select_related('ingredient_id')

    # If no allergies are found
    if not allergies.exists():
        custAllergies = {"message": "No allergies! :)"}
    else:
        custAllergies = [
            {
                "iupac_name": allergy.ingredient_id.iupac_name,
                "common_name": allergy.ingredient_id.common_name
            }
            for allergy in allergies
        ]

    try:
        custInsurance = InsurancePlan.objects.get(cust_healthcare_id=custHealthID).health_insurance_field
    except InsurancePlan.DoesNotExist:
        custInsurance = 'No insurance plan'

    data = {
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone": custPhone,
        "email": custEmail,
        "allergies": custAllergies,
        "healthcare_id": customer.alberta_healthcare_id,
        "insurance_plan": custInsurance,

    }
    return JsonResponse(data)


    