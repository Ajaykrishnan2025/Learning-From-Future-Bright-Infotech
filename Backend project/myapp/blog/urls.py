from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.index, name="index"),
    # path("post/<str:slug>/", views.detail, name="detail"),
    path("service/", views.service, name="service"),
    path("register/", views.register, name="register"),
    path("contact", views.contact, name="contact"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("forgot_password/", views.forgot_password, name="forgot_password"), 
    # path("dashboard/", views.dashboard, name="dashboard"),
]