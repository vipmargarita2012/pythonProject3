from django.urls import path
# Импортируем созданное нами представление
from .views import (
    PostList, PostDetail, PostCreate, PostUpdate, PostDelete, ProfileAuthorUpdate, Category, CategoryList, index,
)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('post_list/', index, name='index'),
    path('category/<int:pk>', Category.as_view(), name='category_detail'),
    path('cats/', CategoryList.as_view(), name='cats'),
    path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name ='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('profile/<int:pk>/update/', ProfileAuthorUpdate.as_view(), name='edit_profile'),
]