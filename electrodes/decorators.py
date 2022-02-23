from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.groups.all():
                if request.user.groups.all()[0].name in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, "page-404.html")
        return wrap
    return decorator


def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.profile.userStatus == "admin":
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "dashboard/404.html")
    return wrap
