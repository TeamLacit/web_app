from django.http import Http404
from django.shortcuts import render, redirect
from user.forms import ChangeDataUserForm, CalendarForm, ChangePasswordUserForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from datetime import date
from user.calendar import get_all_weeks_month, years, months
from user.models import Task


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
        "today": today,
    })


def tasks(request, year, month, day):
    """Список заданий на определенный день"""
    if year in years and month in [i for i in range(1, 13)] and 1 <= day <= 31:
        try:
            get_date = date(year, month, day)
            return render(request, "user/tasks.html", context={
                "date": get_date,
                "tasks": Task.objects.filter(user__id=request.user.id, date=get_date),
            })
        except ValueError:
            raise Http404()
    else:
        raise Http404()


def change_password_user(request):
    """Смена пароля пользователя"""
    if request.method == "POST":
        form = ChangePasswordUserForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            if not check_password(old_password, request.user.password):
                message = "wrong old password"
                return render(request, "user/change_password_user.html", context={"form": form, "err_message": message})
            request.user.set_password(form.cleaned_data["password"])
            request.user.save()
            return redirect("/accounts/login")
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
