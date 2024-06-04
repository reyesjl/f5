from django.urls import path
from . import views

urlpatterns = [
    # health home
    path("", views.index, name="health-home"),

    # posts
    path("posts/", views.post_list, name="post-list"),
    path("posts/create/", views.post_create, name="post-create"),
    path("posts/<slug:post_slug>/", views.post_detail, name="post-detail"),
    path("posts/<slug:post_slug>/update/", views.post_update, name="post-update"),
    path("posts/<slug:post_slug>/delete/", views.post_delete, name="post-delete"),
]