from django.shortcuts import render
from django.views.decorators.http import require_POST

def index(request):
    pass


@require_POST
def create_task(request):
    """Сохраняет отправленный с формы task в БД"""
