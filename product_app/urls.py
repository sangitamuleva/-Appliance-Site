from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('register/', views.registerPage, name='register'),
    path('product/', views.productPage, name='product'),
    path('customer/', views.customerPage, name='customer'),
    path('', views.homePage, name='home')
]