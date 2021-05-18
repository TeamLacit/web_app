from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    """Главная страница"""
    return HttpResponseRedirect("/authorization")
