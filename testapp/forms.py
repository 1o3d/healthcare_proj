from django import forms
from django.forms import ModelForm
from .models import  Customer, Medication, CustomerPhone, CustomerEmail, InsurancePlan, MedicationIngredients
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

class SignupForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

class AddCustRepForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ["password", "healthcare_rep"]

class LinkCustForm(forms.Form):
    AB_id = forms.CharField(required=True, max_length=10)
    Fname = forms.CharField(max_length=100, required=True)
    Lname = forms.CharField(max_length=100, required=True)

class MedForm(ModelForm):
    class Meta:
        model = Medication
        fields = ['med_name','needs_prescription']

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username','address']

class CustPhoneForm(forms.ModelForm):
    class Meta:
        model = CustomerPhone
        fields = ['cust_phone_field']

class CustomerEmailForm(forms.ModelForm):
    class Meta:
        model = CustomerEmail
        fields = ['cust_email']


class CustomerInsuranceForm(forms.ModelForm):
    class Meta:
        model = InsurancePlan
        fields = ['coverage_type']
class IngredientForm(ModelForm):
    class Meta:
        model = MedicationIngredients
        fields = "__all__"
