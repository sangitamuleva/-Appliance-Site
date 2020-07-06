from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('product/', views.productPage, name='product'),
    path('customer/<str:pk>', views.customerPage, name='customer'),
    path('', views.homePage, name='home'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('user/', views.userPage, name='user_home'),
    path('account/', views.account_settingPage, name='account_setting'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='Accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='Accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='Accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset_done.html'), name='password_reset_complete'),

]
