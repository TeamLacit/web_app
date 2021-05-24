from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user.models import User


def decorator_check_director(func):
    """"Декоратор для проверки роли руководителя"""
    def wrapped(request, **kwargs):
        if request.user.role == 2:
            return func(request, **kwargs)
        else:
            return redirect("/accounts/login")
    return wrapped


# @decorator_check_director
#@login_required
def index(request):
    return render(request, "director/index.html", context={
#        "users": request.user.department.user_set.filter(role=3)
    })

