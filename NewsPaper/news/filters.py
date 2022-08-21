from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter
from django.forms import DateInput
from .models import Post,  Author

# Создаем свой набор фильтров для модели Post.

class PostFilter(FilterSet):
    date = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        label='Create after',
        widget=DateInput(
        attrs={'type': 'date'}
        )
    )
    title = CharFilter(lookup_expr='icontains')

    author = ModelChoiceFilter(queryset=Author.objects.all())

    date.field.error_massages = {'invalid': 'Enter date in format DD.MM.YYYY'}

class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
    model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
    fields = ['date', 'title', 'author']
