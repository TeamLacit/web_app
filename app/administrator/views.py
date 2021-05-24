from django.shortcuts import render, redirect

from administrator.models import UnregisteredUser
from administrator.forms import InvitationForm


def index(request):
    """Главная страница админа"""
    return render(request, "admin/index.html")


def invite_user(request):
    """Приглашение пользователя на регистрацию"""
    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            user = UnregisteredUser()
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.department = form.cleaned_data["department"]
            user.post = form.cleaned_data["post"]
            user.role = 3
            user.save()
            return redirect(index)
    else:
        form = InvitationForm()
    return render(request, "admin/invitation.html", context={"form": form})

