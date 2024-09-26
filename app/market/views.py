from django.shortcuts import redirect, render
from .models import Product
from .forms import CreateProductForm
from core.decorators import is_admin
from django.contrib.auth.decorators import user_passes_test

def index(request):
    products = Product.objects.filter(available=True)
    context = {
        'products': products,
    }
    return render(request, "market/index.html", context)

@user_passes_test(is_admin)
def create_product(request):
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('market-index')
    else:
        form = CreateProductForm()
    
    context = {
        'form': form,
    }

    return render(request, 'market/create_product.html', context)