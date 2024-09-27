from django.urls import path
from .views import *

urlpatterns = [
    path("products/", ProductListView.as_view(), name="list_products"),
    path('products/create/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='detail_product'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
]