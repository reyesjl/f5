from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="market_index"),
    path("create_product/", views.create_product, name="create_product")
]