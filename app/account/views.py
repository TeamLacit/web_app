from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login as impl_login, logout as impl_logout
from django.contrib import messages



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


def registration(request, id):
    form = RegisterForm()
    return render(request, "account/registration.html", context={"form": form})
