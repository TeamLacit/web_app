from django.shortcuts import render, redirect
from user.forms import ChangeDataUserForm
from django.contrib import messages


def index(request):
    """Главная страница пользователя"""
    return render(request, "user/index.html")


def change_data_user(request):
    """Редактирование данных пользователем"""
    if request.method == "POST":
        form = ChangeDataUserForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data["email"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.save()
            return redirect(index)
        else:
            messages.error(request, "Invalid data")
    form = ChangeDataUserForm(instance=request.user)
    return render(request, "user/change_data_user.html", context={"form": form})
