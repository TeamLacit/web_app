from django.shortcuts import render


def authorization(request):
    """Авторизация"""
    return render(request, "index.html")
