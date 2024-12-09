from django.urls import path
from .import views


urlpatterns = [
    path('testapp/hello', views.view_pharm),
    # path('home/', views.home),
    path('',views.home, name = 'home'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logging_out, name = 'logging_out'),
    path('signup/', views.signup, name = 'signup'),
    path('user/', views.user, name = 'user'),
    path('healthrep/', views.healthrep, name = 'healthrep'),
    path('distrib/', views.distrib, name = 'distrib'),
    path('distrib_signup/', views.distrib_signup, name = 'distrib_signup'),
    path('representative_signup/', views.representative_signup, name = 'representative_signup'),
    path('customer/<str:customer_username>/', views.customer_details, name='customer_details'),
    path('healthrep/<str:username>/edit', views.edit_customer, name='edit_customer'),
    path('user_create_allergy/', views.user_create_allergy, name='user_create_allergy'),
    path('user_delete_allergy/', views.user_delete_allergy, name='user_delete_allergy'),
    path('user_create_pres/', views.user_create_pres, name='user_create_pres'),
    path('user_delete_pres/', views.user_delete_pres, name='user_delete_pres'),
    path('user_create_insurance/', views.user_create_insurance, name='user_create_insurance'),
    path('user_delete_insurance/', views.user_delete_insurance, name='user_delete_insurance'),
    path('user_create_coverage/', views.user_create_coverage, name='user_create_coverage'),
    path('user_delete_coverage/', views.user_delete_coverage, name='user_delete_coverage')

]