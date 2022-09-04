from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Author

class PostForm(forms.ModelForm):
    description = forms.CharField(min_length=20)
    title = forms.CharField(max_length=128)
    # categories = forms.ChoiceField()
    class Meta:
        model = Post
        fields = ['title', 'postCategory', 'categoryType', 'text']

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return title

class ProfileAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['authorUser']