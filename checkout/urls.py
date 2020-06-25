from django.urls import path

from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("charge", views.charge, name="charge"),
    path("success/<str:args>", views.success_page, name="success"),
]