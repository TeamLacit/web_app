from django.forms import Form, DateField, ModelMultipleChoiceField
from user.calendar import years
from user.models import User
from datetime import date

class SelectionForm(Form):
    start_date = DateField(label='From', input_formats=['%d/%m/%Y'])
    end_date = DateField(label='To', input_formats=['%d/%m/%Y'])
    users = ModelMultipleChoiceField(queryset=User.objects.filter(role=3))

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super(SelectionForm, self).__init__(*args, **kwargs)

        if self.department:
            self.fields['users'].queryset = User.objects.filter(role=3, department=self.department)

    def is_valid(self):
        valid = super(SelectionForm, self).is_valid()

        if not valid:
            return valid

        for user in self.cleaned_data['users']:
            if user.department != self.department:
                return False

        get_start_date, get_end_date = self.cleaned_data['start_date'], self.cleaned_data['end_date']

        if get_start_date >= get_end_date or get_start_date.year < years[-1] or get_end_date > date.today():
            return False

        return True
