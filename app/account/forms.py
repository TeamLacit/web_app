from django.forms import Form, EmailField, PasswordInput, CharField, ValidationError


class LoginForm(Form):
    email = EmailField()
    password = CharField(widget=PasswordInput)


class RegisterForm(Form):
    password = CharField(label="new password", widget=PasswordInput)
    password2 = CharField(label="repeat password", widget=PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("passwords don't match")
        return cd['password2']
