from django.http import Http404
from django.shortcuts import render, redirect
from user.forms import ChangeDataUserForm, CalendarForm, ChangePasswordUserForm, TaskForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from datetime import date
from user.calendar import get_all_weeks_month, years, months
from user.models import Task


def decorator_check_user(func):
    """"Декоратор для проверки роли пользователя"""
    def wrapped(request, **kwargs):
        if request.user.role == 3:
            return func(request, **kwargs)
        else:
            return redirect("/accounts/login")
    return wrapped


def decorator_check_date(func):
    """Декоратор для проверки даты"""
    def wrapped(request, year, month, day):
        if year in years and month in [i for i in range(1, 13)] and 1 <= day <= 31:
            try:
                return func(request, year, month, day)
            except ValueError:
                raise Http404()
        else:
            raise Http404()
    return wrapped


def decorator_handles_task_DoesNotExist(func):
    """Декоратор обрабатывайщий исключение Task.DoesNotExist"""
    def wrapped(request, **kwargs):
        try:
            return func(request, **kwargs)
        except Task.DoesNotExist:
            raise Http404()
    return wrapped


@login_required
@decorator_check_user
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

@login_required
@decorator_check_user
@decorator_check_date
def tasks(request, year, month, day):
    """Список заданий на определенный день"""
    get_date = date(year, month, day)
    return render(request, "user/tasks.html", context={
        "date": get_date,
        "tasks": Task.objects.filter(user__id=request.user.id, date=get_date),
    })


@login_required
@decorator_check_user
def change_password_user(request):
    """Смена пароля пользователя"""
    if request.method == "POST":
        form = ChangePasswordUserForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            if not check_password(old_password, request.user.password):
                messages.error(request, "wrong old password!")
                return render(request, "user/change_password_user.html", context={"form": form})
            request.user.set_password(form.cleaned_data["password"])
            request.user.save()
            return redirect("/accounts/login")
    else:
        form = ChangePasswordUserForm()
    return render(request, "user/change_password_user.html", context={"form": form})


@login_required
@decorator_check_user
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


@login_required
@decorator_check_user
@decorator_check_date
def create_task(request, year, month, day):
    """Добавления задания"""
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            Task.objects.create(**{
                "project": form.cleaned_data["project"],
                "time_worked": form.cleaned_data["time_worked"],
                "description": form.cleaned_data["description"],
                "date": date(year, month, day),
                "user": request.user,
            })
            return redirect(tasks, year, month, day)
        else:
            messages.error(request, "Invalid data")
    return render(request, "user/task_form.html", context={
        "form": TaskForm(user=request.user),
        "button_name": "Create",
    })


@login_required
@decorator_check_user
@decorator_handles_task_DoesNotExist
def edit_task(request, task_id):
    """Редактирование задания"""
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            Task.objects.filter(id=task_id, user=request.user).update(**{
                "project": form.cleaned_data["project"],
                "time_worked": form.cleaned_data["time_worked"],
                "description": form.cleaned_data["description"],
            })
            task = Task.objects.get(id=task_id, user=request.user)
            return redirect(tasks, task.date.year, task.date.month, task.date.day)
        else:
            messages.error(request, "Invalid data")
    return render(request, "user/task_form.html", context={
        "form": TaskForm(user=request.user, instance=Task.objects.get(id=task_id, user=request.user)),
        "button_name": "Edit",
    })


@login_required
@decorator_check_user
@decorator_handles_task_DoesNotExist
def delete_task(request, task_id):
    """Удаление задания"""
    task = Task.objects.get(id=task_id, user=request.user)
    year, month, day = task.date.year, task.date.month, task.date.day
    task.delete()
    return redirect(tasks, year, month, day)
