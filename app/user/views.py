from django.shortcuts import render, redirect
from user.forms import ChangeDataUserForm, CalendarForm, ChangePasswordUserForm
from django.contrib import messages
from datetime import date
from user.calendar import get_all_weeks_month, years, months


def index(request):
    """Главная страница пользователя"""
    today = date.today()

    if request.method == "POST":
        form = CalendarForm(request.POST)
        if form.is_valid():
            year, month = form.cleaned_data["year"], months.index(form.cleaned_data["month"]) + 1
        else:
            year, month = today.year, today.month
    else:
        year, month = today.year, today.month

    weeks = get_all_weeks_month(year, month)

    return render(request, "user/index.html", context={
        "years": years,
        "current_year": year,
        "current_month": month,
        "months": months,
        "weeks": weeks,
    })


def tasks(request):
    """Список заданий на определенный день"""
    return render(request, "user/tasks.html")


def change_password_user(request):
    """Смена пароля пользователя"""
    if request.method == "POST":
        form = ChangePasswordUserForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["password"])
            request.user.save()
            return redirect(index)
    else:
        form = ChangePasswordUserForm()
    return render(request, "user/change_password_user.html", context={"form": form})


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
