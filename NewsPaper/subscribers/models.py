from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")
    post_category = forms.CharField(label="Категория")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            )


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user








# from django.db import models
# from datetime import datetime
#
# class Subscribers(models.Model):
#     date = models.DateField(default=datetime.utcnow,)
#     client_name = models.CharField(max_length=200)
#     message = models.TextField()
#
#     def __str__(self):
#         return f'{self.client_name} : {self.message}'

