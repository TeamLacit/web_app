from django import forms

from administrator.models import UnregisteredUser


class InvitationForm(forms.ModelForm):
    class Meta:
        model = UnregisteredUser
        fields = ['first_name', 'last_name', 'email', 'department', 'post']