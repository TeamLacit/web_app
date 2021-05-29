from django import forms

from administrator.models import UnregisteredUser


class InvitationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=((2, 'director'), (3, 'user')))

    class Meta:
        model = UnregisteredUser
        fields = ['first_name', 'last_name', 'email', 'department', 'post']
