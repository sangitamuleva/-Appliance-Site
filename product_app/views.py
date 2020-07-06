from django.shortcuts import render, redirect
from .forms import CreateUserForms, OrderForm,CustomerForm
from .models import *
from django.forms import inlineformset_factory
from .filters import OrderFilter
from .decorators import unauthenticated_user, admin_only, allowed_users
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForms()

    if request.method == 'POST':
        form = CreateUserForms(request.POST)

        if form.is_valid():
            # save data in database
            user = form.save()


            # get user
            user_name = form.cleaned_data.get('username')
            messages.success(request, "Registration is completed for user " + user_name)
            return redirect('login')
    context = {"form": form}
    return render(request, 'User_Auth/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username Or Password Is Incorrect')

    context = {}
    return render(request, 'User_Auth/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def productPage(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'Accounts/products.html', context)


@login_required(login_url='login')
@admin_only
def homePage(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {"orders": orders,
               "customers": customers,
               "total_customer": total_customer,
               "total_orders": total_orders,
               "delivered": delivered, "pending": pending}
    return render(request, 'Accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customerPage(request, pk):
    customer = Customer.objects.get(id=pk)
    customer_order = customer.order_set.all()

    myfilter = OrderFilter(request.GET, queryset=customer_order)
    customer_order = myfilter.qs
    total_order = customer_order.count()
    context = {"customer": customer, "orders": customer_order, "total_order": total_order, 'myfilter': myfilter}
    return render(request, 'Accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    # multiple form set
    OrderFormatSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))

    customer = Customer.objects.get(id=pk)

    formset = OrderFormatSet(queryset=Order.objects.none(), instance=customer)
    # form=OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # form=OrderForm(request.POST)
        formset = OrderFormatSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {"formset": formset}
    return render(request, 'Accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order_by_id = Order.objects.get(id=pk)
    form = OrderForm(instance=order_by_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order_by_id)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form": form}
    return render(request, 'Accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order_by_id = Order.objects.get(id=pk)

    if request.method == 'POST':
        order_by_id.delete()
        return redirect('/')
    context = {"order": order_by_id}
    return render(request, 'Accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {"orders": orders, "total_orders": total_orders, "delivered": delivered, "pending": pending}
    return render(request, 'Accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settingPage(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)

    if request.method =='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {"form":form}
    return render(request, 'Accounts/account_settings.html', context)
