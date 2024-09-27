from django.http import Http404
from .models import Product
from .forms import ProductForm
from core.decorators import is_admin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

class ProductListView(ListView):
    """View to list all available products."""
    model = Product
    template_name = 'market/products/list_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Returns a queryset of products that are available."""
        return Product.objects.filter(available=True)

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ProductCreateView(CreateView):
    """View to create a new product."""
    model = Product
    form_class = ProductForm
    template_name = 'market/products/create_product.html'
    success_url = reverse_lazy('list_products')

class ProductDetailView(DetailView):
    """View to display the details of a specific product."""
    model = Product
    template_name = 'market/products/detail_product.html'
    context_object_name = 'product'

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ProductUpdateView(UpdateView):
    """View to update an existing product."""
    model = Product
    form_class = ProductForm
    template_name = 'market/products/update_product.html'
    success_url = reverse_lazy('list_products')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ProductDeleteView(DeleteView):
    """View to delete an existing product."""
    model = Product
    template_name = 'market/products/delete_product.html'
    success_url = reverse_lazy('list_products')