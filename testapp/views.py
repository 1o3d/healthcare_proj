from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def view_pharm(request):
    return HttpResponse('Hello World')