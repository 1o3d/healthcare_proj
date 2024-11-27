from django.urls import path
from .import views


urlpatterns = [
    path('testapp/hello', views.view_pharm),
    # path('home/', views.home),
    path('',views.home, name = 'home'),
    path('login/', views.login, name = 'login')
]