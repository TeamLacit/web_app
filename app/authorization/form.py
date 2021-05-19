from authorization.models import Account
from django.forms import ModelForm


class LoginForm(ModelForm):
    class Meta:
        model = Account
        fields = ["email", "password"]
