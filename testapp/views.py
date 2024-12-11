from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *
from django.db.models import Subquery
from django.contrib import messages
from django.db import IntegrityError
import datetime
from hashlib import sha256

# Create your views here.
def view_pharm(request):
    return HttpResponse('Hello World')

def encode(password):
    return sha256(password.encode('utf-8')).hexdigest()


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
            hashed = encode(form_password)

            try:
                invalidCred = False
                 # https://docs.djangoproject.com/en/5.1/topics/db/queries/
                cust_user = Customer.objects.get(username = form_username, password=hashed)   # Syntax: <variable name> = <model name>.objects.get(<dbcolumn=value>)
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
                    rep_user = HealthCareRepresentative.objects.get(username = form_username, password=hashed)
                    print(rep_user.first_name + ' ' + rep_user.last_name)
                    request.session['username'] = form_username
                    request.session['usertype'] = 2
                    return redirect('healthrep')
                except HealthCareRepresentative.DoesNotExist:
                    # invalidCred = True
                    print("Invalid rep username")

                    # check for distributer
                    try:
                        dist_user = Distributer.objects.get(username = form_username, password=hashed)
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
            password = form.cleaned_data['password']
            hashed = encode(password)

            user = form.save(commit=False)
            user.password = hashed
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request,'signup.html', {'form':form})

def distrib_signup(request):
    if request.method == 'POST':
        form = DistributerSignupForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            hashed = encode(password)

            distributer = form.save(commit=False)
            distributer.password = hashed
            distributer.save()
            return redirect('login')
    else:
        form = DistributerSignupForm()
    return render(request,'distrib_signup.html',{'form':form})

def representative_signup(request):
    if request.method == 'POST':
        form = RepresentitiveSignupForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            hashed = encode(password)

            representative = form.save(commit=False)
            representative.password = hashed
            representative.save()
            return redirect('login')
    else:
        form = RepresentitiveSignupForm()
    return render(request,'representative_signup.html',{'form':form})

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
    allergic_meds = Medication.objects.filter(
        med_name__in=Subquery(
            MedicationIngredients.objects.filter(
                iupac_name__in=Subquery(
                    allergies.values('ingredient_id')
                )
            ).values('med_name')
        )
    )
    inventories = Inventory.objects.all()
    orders = PrescriptionOrder.objects.filter(cust_healthcare_id=cust_id)

    returnstruct = {
        'logged_in': request.session.get('username', default = None),
        'ingredients': ingredients,
        'allergies': allergies,
        'prescriptions': prescriptions,
        'plans': insurance,
        'covs': coverages,
        'meds': presc_meds,
        'allrgmeds': allergic_meds,
        'inventories': inventories,
        'orders': orders,
    }
    print(orders)
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
            try:
                Allergy.objects.create(symptoms=symptoms_text,cust_healthcare_id=cust_id,ingredient_id=ingredients_id)
            except IntegrityError:
                messages.error(request, "ERROR: That symptom already exists! Try another name.")
    return redirect('user')

def user_delete_allergy(request):
    if request.method == "POST":
        todelete = request.POST.get('delbutton')
        print("deleting " + todelete)
        try:
            Allergy.objects.filter(pk=todelete).delete()
        except IntegrityError:
            messages.error(request, "ERROR: Error deleting allergy. Does something rely on it?")
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
            try:
                Prescription.objects.create(cust_healthcare_id=cust_id,prescription_name=pname,refill_date=refdate,dosage=pdosage,rx_number=rxnum)
            except IntegrityError:
                messages.error(request, 'ERROR: Rx number is already being used!')
    return redirect('user')

def user_delete_pres(request):
    if request.method == "POST":
        todelete = request.POST.get('presdelbutton')
        print("deleting " + todelete)
        try:
            Prescription.objects.filter(rx_number=todelete).delete()
        except IntegrityError:
            messages.error(request, "ERROR: An order or coverage relies on this prescription, please delete those first!")
    return redirect('user')

def user_create_insurance(request):
    cust_id = Customer.objects.get(username = request.session['username'])
    if request.method == "POST":
        coveragetype = request.POST.get('insurancetypeinput')
        if coveragetype:
            try :
                InsurancePlan.objects.create(coverage_type=coveragetype,cust_healthcare_id=cust_id)
            except IntegrityError:
                print("INTEGRITY ERROR IN INSURANCE")
                messages.error(request, 'ERROR: Coverage type already exists.')
    return redirect('user')

def user_delete_insurance(request):
    if request.method == "POST":
        todelete = request.POST.get('plandelbutton')
        try:
            InsurancePlan.objects.filter(health_insurance_field=todelete).delete()
        except IntegrityError:
            messages.error(request, "ERROR: Cannot delete insurance. Please check if something depends on it.")
    return redirect('user')

def user_create_coverage(request):
    cust_id = Customer.objects.get(username = request.session['username'])
    if request.method == "POST":
        insplan = InsurancePlan.objects.get(health_insurance_field=request.POST.get('insselect'))
        rxnum = Prescription.objects.get(rx_number=request.POST.get('covpres'))
        covamt = request.POST.get('covperc')

        if insplan and rxnum and covamt:
            try:
                InsuranceCoverage.objects.create(health_insurance_field=insplan,rx_number=rxnum,coverage_amount=covamt,cust_healthcare_id=cust_id)
            except IntegrityError:
                print("COVERAGE INTEGRITY ERROR")
                messages.error(request, 'ERROR: Plan already has a coverage assigned.')
    return redirect('user')

def user_make_order(request):
    cust_id = Customer.objects.get(username = request.session['username'])
    if request.method == "POST": 
        inventory = Inventory.objects.get(inv_id = request.POST.get('orderbutton'))
        orderpres = Prescription.objects.get(rx_number = request.POST.get('orderpres'))
        ord_date = datetime.date.today()
        exp_date = ord_date + datetime.timedelta(days=30)

        if inventory  and orderpres and ord_date and exp_date:
            try:
                PrescriptionOrder.objects.create(rx_number=orderpres,cust_healthcare_id=cust_id,inv_id=inventory,order_date=ord_date,expiry_date=exp_date)
            except IntegrityError:
                messages.error(request, "ERROR: You've already made an order for this prescription!")
                print("order integrity error")
    return redirect('user')

def user_cancel_order(request):
    cust_id = Customer.objects.get(username = request.session['username'])
    if request.method == "POST": 
        order = request.POST.get('ordercancelbutton')
        if order:
            try:
                PrescriptionOrder.objects.filter(rx_number=order).delete()
            except IntegrityError:
                messages.error(request, "ERROR: Cannot cancel order, error occured.")

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

    # Ingredients list:
    ingredients = Ingredient.objects.all()

    #selected_med = request.GET.get('medication')
    #print(f"Selected Medication: {selected_med}")

    if request.method == 'POST':
        med_form = MedForm(request.POST)
        ing_form = IngredientForm(request.POST)
        med_ing_form = MedIngredientForm(request.POST)
        if med_form.is_valid():
            # https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/#:~:text=If%20you%20call%20save(),on%20the%20resulting%20model%20instance.
            # The form is created but not saved, we still need to input the dist id attribute
            medication = med_form.save(commit=False)
            # Although it's a foreign key of type CHAR. This is actually asking for a distributer to be assigned to.
            medication.distributer_id = dist_user
            if(medication.med_name != ""):
                medication.save() #Add the medication
        if ing_form.is_valid():
            ing_form.save()

        if med_ing_form.is_valid():
            medication_ingredient = med_ing_form.save(commit=False)
            medication_ingredient.distributer_id = dist_user
            medication_ingredient.save()
    else:
        med_form = MedForm()
        ing_form = IngredientForm()
        med_ing_form = MedIngredientForm()
    # send over the re;evant medications for render
    return render(request,'distrib.html',
        {
            'logged_in': request.session.get('username', default = None), 
            'meds':dist_medications,
            'add_med_form':med_form,
            'add_ing_form':ing_form,
            'add_med_ing_form':med_ing_form,
            'inventories':dist_inventories,
            'med_ingredients':list(med_ingredients),
            'all_ingredients':ingredients
        })

def delete_med(request):
    if request.method == "POST":
        todelete = request.POST.get('del_med_button')
        Medication.objects.filter(pk=todelete).delete()
    return redirect('distrib')

def delete_med_ing(request):
    if request.method == "POST":
        medication = request.POST.get('del_med_ing')
        ingredient = request.POST.get('selected_ing')
        # delete filtered med ingredients
        filtered_meds = MedicationIngredients.objects.filter(med_name=medication)
        filtered_meds.get(iupac_name = ingredient.strip()).delete()
        
    return redirect('distrib')

def delete_ing(request):
    if request.method == "POST":
        ingredient = request.POST.get('del_ing')
        Ingredient.objects.get(iupac_name=ingredient).delete()
        
    return redirect('distrib')

def supply_inventory(request):
    if request.method == "POST":
        qty = request.POST.get('Qty')
        inventory = request.POST.get('supply_inv_button')
        
        # delete filtered med ingredients
        selected_inventory = Inventory.objects.get(inv_id = inventory)

        print("Selected_in id:" + str(selected_inventory.inv_id) + "\tamount_left: " + str(selected_inventory.amount_left))
        selected_inventory.amount_left = selected_inventory.amount_left + int(qty)
        selected_inventory.save()

    return redirect('distrib')

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

    # allergies = Allergy.objects.filter(cust_healthcare_id=custHealthID).select_related('ingredient_id')

    # # If no allergies are found
    # if not allergies.exists():
    #     custAllergies = {"message": "No allergies! :)"}
    # else:
    #     custAllergies = [
    #         {
    #             "iupac_name": allergy.ingredient_id.iupac_name,
    #             "common_name": allergy.ingredient_id.common_name
    #         }
    #         for allergy in allergies
    #     ]


    try:
        custAllList = []
        custAllergy = Allergy.objects.filter(cust_healthcare_id=custHealthID)
        for i in custAllergy:
            ing = Ingredient.objects.filter(allergy=i)
            for j in ing:
                custAllList.append(j.common_name)

    except Allergy.DoesNotExist:
        custAllergies = 'No allergies :)'

    try:
        custInsList = []
        custInsurance = InsurancePlan.objects.filter(cust_healthcare_id=custHealthID)
        for i in custInsurance:
            custInsList.append(i.coverage_type)
    except InsurancePlan.DoesNotExist:
        custInsurance = 'No insurance plan'

    data = {
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone": custPhone,
        "email": custEmail,
        "allergies": custAllList,
        "healthcare_id": customer.alberta_healthcare_id,
        "insurance_plan": custInsList,

    }
    return JsonResponse(data)


def edit_customer(request, username):
    customer = get_object_or_404(Customer, username=username)
    try:
        customer_phone = CustomerPhone.objects.get(alberta_healthcare_id=customer.alberta_healthcare_id)
    except CustomerPhone.DoesNotExist:
        customer_phone = None

    try:
        customer_email = CustomerEmail.objects.get(alberta_healthcare_id=customer.alberta_healthcare_id)
    except CustomerEmail.DoesNotExist:
        customer_email = None

    try:
        customer_insurance = InsurancePlan.objects.get(cust_healthcare_id=customer.alberta_healthcare_id)
    except InsurancePlan.DoesNotExist:
        customer_insurance = None

    # try:
    #     customer_allergy = []
    #     customer_allergy_List = Allergy.objects.filter(cust_healthcare_id=customer.alberta_healthcare_id)
    #     for i in customer_allergy_List:
    #         ing = Ingredient.objects.get(allergy=i)
    #         customer_allergy.append(ing.ingredient)
    #
    # except Allergy.DoesNotExist:
    #     customer_allergy = None

    if request.method == 'POST':
        # Handle form submission
        customer_form = CustomerEditForm(request.POST, instance=customer)
        phone_formset = CustPhoneForm(request.POST, instance=customer_phone)
        email_formset = CustomerEmailForm(request.POST, instance=customer_email)
        ins_formset = CustomerInsuranceForm(request.POST, instance=customer_insurance)


        if customer_form.is_valid() and phone_formset.is_valid() and email_formset.is_valid():
            customer_instance = customer_form.save(commit=False)
            phone_instance = phone_formset.save(commit=False)
            email_instance = email_formset.save(commit=False)
            ins_instance = ins_formset.save(commit=False)

            phone_instance.alberta_healthcare_id = customer
            email_instance.alberta_healthcare_id = customer
            ins_instance.cust_healthcare_id = customer
            # for field in customer_form.cleaned_data:
            #     if customer_form.cleaned_data[field] not in [None, ""]:
            #         setattr(customer_instance, field, customer_form.cleaned_data[field])
            #
            # for field in phone_formset.cleaned_data:
            #     if phone_formset.cleaned_data[field] not in [None, ""]:
            #         setattr(phone_instance, field, phone_formset.cleaned_data[field])
            #
            # for field in email_instance.cleaned_data:
            #     if email_formset.cleaned_data[field] not in [None, ""]:
            #         setattr(email_instance, field, email_formset.cleaned_data[field])
            # customer_instance.save()
            #
            # phone_formset.save()
            # email_formset.save()
            #
            # return redirect('customer_details', username=customer.username)
            print("Customer instance data:", customer_instance.__dict__)
            print("Phone instance data:", phone_instance.__dict__)
            print("Email instance data:", email_instance.__dict__)
            print("Insurance instance data:", ins_instance.__dict__)
            customer_form.save()
            phone_formset.save()
            email_formset.save()
            ins_formset.save()

            return redirect('/healthrep')
    else:
        # Populate forms with existing data
        customer_form = CustomerEditForm(instance=customer)
        phone_formset = CustPhoneForm(instance=customer_phone)
        email_formset = CustomerEmailForm(instance=customer_email)
        ins_formset = CustomerInsuranceForm(instance=customer_insurance)

    return render(request, 'edit_customer.html', {
        'customer_form': customer_form,
        'phone_formset': phone_formset,
        'email_formset': email_formset,
        'ins_formset': ins_formset,
        'customer': customer,
    })


    
