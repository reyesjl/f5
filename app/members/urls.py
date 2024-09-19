from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logmeout, name='logout'),
]