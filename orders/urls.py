from django.urls import path
from . import views

urlpatterns = [
    path("cart/add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/confirmation/", views.order_confirmation, name="order_confirmation"),
]  