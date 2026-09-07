from django.urls import path
from . import views

urlpatterns = [
    path("tracking/update/", views.update_location, name="update_location"),
    path("tracking/order/<int:order_id>/", views.get_order_location, name="get_order_location"),
] 