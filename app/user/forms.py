from django.forms import ModelForm, Form, IntegerField, CharField
from authorization.models import User
from user.calendar import years, months


class ChangeDataUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ChangePasswordUserForm(ModelForm):
    class Meta:
        model = User
        fields =['password']


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
