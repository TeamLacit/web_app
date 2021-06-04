from django.shortcuts import render, redirect
from django.db.models import RestrictedError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.models import Company, Project
from main.views import decorator_adds_user_information_log
from administrator.views import decorator_check_admin
from project.forms import ProjectForm


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def project_list(request, company_id):
    """Просмотр списка проектов компании"""
    projects = Project.objects.filter(company_id=company_id)
    company = Company.objects.get(id=company_id)
    return render(request, "administrator/project/index.html", context={"projects": projects, "company": company})


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def edit_project(request, company_id, id=None):
    """Добавление и изменение проекта"""
    if id:
        project = Project.objects.get(id=id)
    else:
        project = None

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            if not project:
                project = Project()
            project.name = form.cleaned_data['name']
            project.company = form.cleaned_data['company']
            project.save()
            return redirect(f'/project/list/{company_id}/')
        else:
            messages.error(request, "Invalid data")
    if project:
        form = ProjectForm(instance=project)
    else:
        form = ProjectForm(initial={'company': Company.objects.get(id=company_id)})

    return render(request, "base_form.html", context={
        "form": form,
        "title": "edit project",
        "button_name": "save"
    })


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def delete_project(request, company_id, id):
    """удаление проекта"""
    project = Project.objects.get(id=id)
    if project:
        try:
            project.delete()
        except RestrictedError:
            messages.error(request, f"Can't delete project {project.name}")
    return redirect(f'/project/list/{company_id}')
