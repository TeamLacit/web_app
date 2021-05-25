from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user.models import User, Task
from director.forms import SelectionForm
from django.contrib import messages
from django.http import Http404


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
            start_date, end_date, users = form.cleaned_data["start_date"], form.cleaned_data["end_date"],\
                                          form.cleaned_data["users"]
            return render(request, "director/users_data_selection.html", context={
                "array": {
                    f"{user.first_name} {user.last_name}": Task.objects.filter(user=user).exclude(
                    date__gt=end_date).exclude(date__lt=start_date) for user in users
                }
            })
        else:
            messages.error(request, "Invalid data")
    return render(request, "director/selection_form.html", context={
        "form": SelectionForm(department=request.user.department)
    })
