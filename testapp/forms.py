from django.forms import ModelForm
from .models import  Customer

class LoginForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['username','password']

class SignupForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

