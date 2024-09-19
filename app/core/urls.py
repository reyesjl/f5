from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tours/", views.tours, name="tours-index"),
    path("tour-inquiry/", views.tour_inquiry, name="tour-inquiry"),
    path("agreements/privacy/", views.privacy, name="privacy"),
    path("agreements/terms-of-use/", views.terms_of_use, name="terms-of-use"),
    path("agreements/sales-and-refunds/", views.sales_and_refunds, name="sales-and-refunds"),
    path("agreements/legal/", views.legal, name="legal"),
    path("sitemap/", views.sitemap, name="sitemap"),
    path("contact/", views.contact, name="contact")
]