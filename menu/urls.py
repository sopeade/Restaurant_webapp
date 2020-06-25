from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("access_register", views.access_register, name="access_register"),
    path("register", views.register, name="register"),
    path("access_login", views.access_login, name="access_login"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("total_order", views.total_order, name="total_order"),
    path("cart", views.cart, name="cart"),
]
