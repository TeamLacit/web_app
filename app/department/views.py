from django.shortcuts import render, redirect
from django.db.models import RestrictedError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.models import Company, Department
from main.views import decorator_adds_user_information_log
from administrator.views import decorator_check_admin
from department.forms import DepartmentForm


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def department_list(request, company_id):
    """Просмотр списка отделов компании"""
    departments = Department.objects.filter(company_id=company_id)
    company = Company.objects.get(id=company_id)
    return render(request, "administrator/department/index.html", context={"departments": departments, "company": company})


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def edit_department(request, company_id, id=None):
    """Добавление и изменение отдела"""
    if id:
        department = Department.objects.get(id=id)
    else:
        department = None

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            if not department:
                department = Department()
            department.name = form.cleaned_data['name']
            department.company = Company.objects.get(id=company_id)
            projects = form.cleaned_data['project']
            for project in projects:
                department.project.add(project)
            department.save()
            return redirect(f'/department/list/{company_id}/')
        else:
            messages.error(request, "Invalid data")
    form = DepartmentForm(instance=department)

    return render(request, "base_form.html", context={
        "form": form,
        "title": "edit department",
        "button_name": "save"
    })


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def delete_department(request, company_id, id):
    """удаление отдела"""
    department = Department.objects.get(id=id)
    if department:
        try:
            department.delete()
        except RestrictedError:
            messages.error(request, f"Can't delete department {department.name}")
    return redirect(f'/department/list/{company_id}')