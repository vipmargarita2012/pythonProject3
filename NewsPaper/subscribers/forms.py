from django import forms
from .models import Subscribers


class SubscribersForm(forms.ModelForm):
    #subscribe email form
    class Meta:
        model = Subscribers
        fields = ("email",)
