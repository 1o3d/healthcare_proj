from django.urls import path
from .import views

urlpatterns = [
    path('testapp/hello', views.view_pharm)
]