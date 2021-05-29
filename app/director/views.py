from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user.models import User, Task
from director.forms import SelectionForm
from django.contrib import messages
from django.http import HttpResponse, Http404

import csv
import pandas


def decorator_check_director(func):
    """"Декоратор для проверки роли руководителя"""
    def wrapped(request, **kwargs):
        if request.user.role == 2:
            return func(request, **kwargs)
        else:
            return redirect("/accounts/login")
    return wrapped


@login_required
@decorator_check_director
def index(request):
    """Главная страница руководителя"""
    return render(request, "director/index.html", context={
        "users": User.objects.filter(department=request.user.department, role=3)
    })


@login_required
@decorator_check_director
def user_data(request, user_id):
    """Просмотр данных каждого из пользователей отдела"""
    try:
        get_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404()
    if get_user in User.objects.filter(department=request.user.department, role=3):
        tasks = Task.objects.filter(user=get_user)
        return render(request, "director/user_data.html", context={"get_user": get_user, "tasks": tasks})
    else:
        raise Http404()


@login_required
@decorator_check_director
def users_data_selection(request):
    """Выборка данных пользователей"""
    if request.method == "POST":
        form = SelectionForm(request.POST, department=request.user.department)
        if form.is_valid():
            start_date, end_date, users, file_format = form.cleaned_data["start_date"], form.cleaned_data["end_date"],\
                                          form.cleaned_data["users"], int(form.cleaned_data["uploading_data"])
            array = {user: Task.objects.filter(user=user).exclude(date__gt=end_date).exclude(date__lt=start_date)
                     for user in users}

            column_names = ["First name", "Last name", "Date", "Worked time", "Name project", "Description"]

            if file_format == 1:
                return render(request, "director/users_data_selection.html", context={"array": array})
            elif file_format == 2:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="data.csv"'

                writer = csv.writer(response, delimiter = ";", lineterminator="\r")
                writer.writerow(column_names)
                for user, tasks in array.items():
                    for task in tasks:
                        writer.writerow([user.first_name, user.last_name, str(task.date), task.time_worked,
                                        task.project.name, task.description])
                return response
            else:
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

                data_frame = {column_name: list() for column_name in column_names}
                for user, tasks in array.items():
                    for task in tasks:
                        data_frame["First name"].append(user.first_name)
                        data_frame["Last name"].append(user.last_name)
                        data_frame["Date"].append(str(task.date))
                        data_frame["Worked time"].append(task.time_worked)
                        data_frame["Name project"].append(task.project.name)
                        data_frame["Description"].append(task.description)
                pandas.DataFrame(data_frame).to_excel(response)
                return response
        else:
            messages.error(request, "Invalid data")
    return render(request, "selection_form.html", context={
        "form": SelectionForm(department=request.user.department)
    })
