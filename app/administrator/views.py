from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from user.models import User
from administrator.models import UnregisteredUser
from administrator.forms import InvitationForm


def index(request):
    """Главная страница админа"""
    return render(request, "administrator/index.html")


def invite_user(request):
    """Приглашение пользователя на регистрацию"""
    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            found_email = User.objects.filter(email=form.cleaned_data["email"])
            if not found_email:
                user = UnregisteredUser()
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.email = form.cleaned_data["email"]
                user.department = form.cleaned_data["department"]
                user.post = form.cleaned_data["post"]
                user.role = 3
                user.save()
                send_mail('Регистрация',
                          f'Уважаемый {user.first_name} {user.last_name}, приглашаем вас пройти регистрацию в приложении'
                          f' “Система учета рабочего времени сотрудников”. Для регистрации перейдите по ссылке '
                          f'http://127.0.0.1:8000/accounts/registration/{user.id}/',
                          settings.EMAIL_HOST_USER,
                          [user.email])
                return redirect(index)
            else:
                messages.error(request, "Invalid data")
    else:
        form = InvitationForm()
    return render(request, "administrator/invitation.html", context={"form": form})
