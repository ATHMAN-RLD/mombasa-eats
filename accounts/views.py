from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order

NEXT_STATUS = {
    "paid": "preparing",
    "preparing": "picked_up",
    "picked_up": "en_route",
    "en_route": "delivered",
}


@login_required(login_url="login")
def rider_dashboard(request):
    rider = request.user.rider_profile
    orders = Order.objects.filter(assigned_rider=rider).exclude(status="delivered")
    return render(request, "accounts/dashboard.html", {"orders": orders})


@login_required(login_url="login")
def advance_order_status(request, order_id):
    rider = request.user.rider_profile
    order = get_object_or_404(Order, id=order_id, assigned_rider=rider)
    next_status = NEXT_STATUS.get(order.status)
    if next_status:
        order.status = next_status
        order.save()
    return redirect("rider_dashboard")  