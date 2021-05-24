from django.forms import ModelForm, Form, IntegerField, CharField
from django import forms
from user.models import Task, User
from user.calendar import years, months


class ChangeDataUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ChangePasswordUserForm(Form):
    old_password = forms.CharField(label="old password", widget=forms.PasswordInput)
    password = forms.CharField(label="new password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="repeat password", widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords don't match")
        return cd['password2']


class CalendarForm(Form):
    year = IntegerField(required=False)
    month = CharField(required=False)

    def is_valid(self):
        valid = super(CalendarForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['year'] not in years or self.cleaned_data['month'] not in months:
            return False

        return True


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['time_worked', 'description', 'project']
