from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tours/", views.tours, name="tours_index"),
    path("tour_inquiry/", views.tour_inquiry, name="tour_inquiry"),
    path("agreements/privacy/", views.privacy, name="privacy"),
    path("agreements/terms_of_use/", views.terms_of_use, name="terms_of_use"),
    path("agreements/sales_and_refunds/", views.sales_and_refunds, name="sales_and_refunds"),
    path("agreements/legal/", views.legal, name="legal"),
    path("sitemap/", views.sitemap, name="sitemap"),
    path("contact/", views.contact, name="contact")
]