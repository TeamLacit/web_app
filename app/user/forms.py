from django.forms import ModelForm
from authorization.models import User


class ChangeDataUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ChangePasswordUserForm(ModelForm):
    class Meta:
        model = User
        fields =['password']
