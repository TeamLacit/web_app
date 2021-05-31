from django.shortcuts import render, redirect

import logging


def decorator_adds_user_information_log(func):
    """Добавляет информацию к какому url-адрессу обратился пользователь в журнал"""
    def wrapped(request, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info(f"A user with id={request.user.id} turned to {request.get_full_path()}")
        return func(request, **kwargs)
    return wrapped


@decorator_adds_user_information_log
def index(request):
    """Главное представление приложения"""
    if request.user is not None:
        if request.user.role == 3:
            return redirect("user-page")
        elif request.user.role == 2:
            return redirect("director-page")
        else:
            return redirect("administrator-page")
    else:
        return redirect("login")
