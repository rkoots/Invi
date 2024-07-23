from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('register-supplier', views.CreateSupplier.as_view(), name='register-supplier'),
    path('register-customer', views.CreateCustomer.as_view(), name='register-customer'),
    path('profile', views.ViewProfileDetails, name='profile'),
    ]