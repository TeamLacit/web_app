from django.http import HttpResponseRedirect
from django.shortcuts import render
#from authorization.forms import LoginForm
from django.contrib.auth import authenticate, login as impl_login
from django.contrib import messages


def login(request):
    pass
    """if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data["email"], password=form.cleaned_data["password"])
            if user is not None:
                impl_login(request, user)
                return HttpResponseRedirect("/")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    form = LoginForm()
    return render(request, "login.html", context={"form": form})"""

