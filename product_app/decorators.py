from django.http import HttpResponse
from django.shortcuts import redirect
def unauthenticated_user(view_fun):
    # create wrapper
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_fun(request,*args,**kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):

    def decorator(view_fun):
        def wrapper_func(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_fun(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized")
        return wrapper_func
    return decorator


def admin_only(view_fun):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group =='admin':
            return view_fun(request, *args, **kwargs)

        if group =='customer':
            return redirect('user_home')
        else:
            return HttpResponse("You are not authorized")

    return wrapper_func
