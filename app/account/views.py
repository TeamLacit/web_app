from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as impl_login, logout as impl_logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from account.forms import LoginForm, RegisterForm
from administrator.models import UnregisteredUser
from user.models import User


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data["email"], password=form.cleaned_data["password"])
            if user is not None:
                impl_login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "account/login.html", context={"form": LoginForm()})


@login_required
def logout(request):
    impl_logout(request)
    return redirect(login)


def registration(request):
    """Регистрация пользователей"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]

            try:
                unreg_user = UnregisteredUser.objects.get(code=code)
            except ObjectDoesNotExist:
                messages.error(request, "invalid access key")
                return render(request, "account/registration.html", context={"form": form})

            user = User()
            user.first_name = unreg_user.first_name
            user.last_name = unreg_user.last_name
            user.email = unreg_user.email
            user.department = unreg_user.department
            user.post = unreg_user.post
            user.role = unreg_user.role
            user.set_password(form.cleaned_data["password"])
            user.save()
            unreg_user.delete()
            return redirect("/accounts/login")
    else:
        form = RegisterForm()
    return render(request, "account/registration.html", context={"form": form})
