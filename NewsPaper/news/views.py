from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView,  UpdateView, DeleteView,
)
from .models import Post, Author, Category, PostCategory, CategorySubscribers
from .filters import PostFilter
from .forms import PostForm, ProfileAuthorForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, m2m_changed
from .signals import notify_subscribers_post, categories_changed
from django.contrib import messages

class CategoryList(ListView):
    model = Category
    template_name = 'cats.html'
    context_object_name = 'cats'
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем  класс фильтрации
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем  класс фильтрации
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs.order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['next_publish'] = None
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    # получаем информацию по отдельному посту
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = not self.request.user.groups.filter(name='subscribers').exists()
        context['is_subscribers'] = self.request.user.groups.filter(name='subscribers').exists()
        return context

class Category(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    success_url = '/posts/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        categorySubscribers = CategorySubscribers(
            category_id = self.get_object().id,
            user = self.request.user,
        )
        try:
            categorySubscribers.save()
            messages.success(request, f'Вы успешно подписались на раздел {self.get_object().name}')
        except:
            messages.error(request, f'Вы уже подписаны на раздел {self.get_object().name}')
        return redirect('post_list')

class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    success_url = '/posts/'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get(authorUser=self.request.user)
        # Сохраним новый пост в базе данных
        result = super().form_valid(form)
        # Дождемся сигнала, когда в базу запишутся разделы новой статьи, чтобы можно было отправить уведомления их подписчикам
        m2m_changed.connect(categories_changed, sender=Post.postCategory.through)

        return result

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'



class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ProfileAuthorUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileAuthorForm
    model = Author
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('post_list')


