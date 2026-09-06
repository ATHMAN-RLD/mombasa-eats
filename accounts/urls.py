from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", views.rider_dashboard, name="rider_dashboard"),
    path("dashboard/order/<int:order_id>/advance/", views.advance_order_status, name="advance_order_status"),
] 