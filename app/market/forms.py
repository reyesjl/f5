from django import forms
from .models import Product

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'image',
            'price',
            'category',
            'stock_quantity',
            'available',
            'featured'
        ]