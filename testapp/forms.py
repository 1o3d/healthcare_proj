from django import forms
from django.forms import ModelForm
from .models import Customer, Medication, MedicationIngredients

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

class SignupForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

class MedForm(ModelForm):
    class Meta:
        model = Medication
        fields = ['med_name','needs_prescription']

class IngredientForm(ModelForm):
    class Meta:
        model = MedicationIngredients
        fields = "__all__"
