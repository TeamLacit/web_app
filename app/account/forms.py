from django.forms import Form, EmailField, PasswordInput, CharField


class LoginForm(Form):
    email = EmailField()
    password = CharField(widget=PasswordInput)
