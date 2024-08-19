from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def admin_check(user):
    return user.is_superuser

def admin_check(user):
    return user.is_authenticated

def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if admin_check(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login")
    return _wrapped_view