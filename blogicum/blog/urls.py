from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path(
        'posts/create/',
        views.post_edit,
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.post_edit,
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.post_delete,
        name='delete_post'
    ),
    path(
        'profile/<slug:username>/',
        views.Profile.as_view(),
        name='profile'
    ),
    path(
        'profile/<slug:username>/edit/',
        views.edit_profile,
        name='edit_profile'
    ),
    path(
        'create_shelf',
        views.create_shelf,
        name='create_shelf'
    ),
    path(
        'create_author',
        views.create_author,
        name='create_author'
    )
]
