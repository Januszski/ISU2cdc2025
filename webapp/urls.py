from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("request-download/", views.request_download, name="request_download"),
    path("login/", auth_views.LoginView.as_view(template_name="webapp/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('download-ready/<str:token>/', views.download_ready, name='download_ready'),

]