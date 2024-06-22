from django.urls import path
from . import views

urlpatterns = [
    # blog home
    path("", views.index, name="blog-home"),

    # articles
    #path("articles/", views.article_list, name="article-list"),
    path("articles/create/", views.article_create, name="article-create"),
    path("articles/<slug:slug>/", views.article_detail, name="article-detail"),
    path("articles/<slug:slug>/update/", views.article_update, name="article-update"),
    path("articles/<slug:slug>/delete/", views.article_delete, name="article-delete"),
]