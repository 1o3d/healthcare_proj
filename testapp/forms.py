from django import forms
from django.forms import ModelForm
from .models import  Customer

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
        fields = ['med_name']