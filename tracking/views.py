import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import RiderLocation


@login_required(login_url="login")
@csrf_exempt
@require_POST
def update_location(request):
    rider = request.user.rider_profile
    data = json.loads(request.body)
    latitude = data["latitude"]
    longitude = data["longitude"]

    RiderLocation.objects.update_or_create(
        rider=rider,
        defaults={"latitude": latitude, "longitude": longitude},
    )
    return JsonResponse({"status": "ok"})


def get_order_location(request, order_id):
    from orders.models import Order
    order = Order.objects.get(id=order_id)
    if not order.assigned_rider:
        return JsonResponse({"error": "No rider assigned yet"}, status=404)

    try:
        location = order.assigned_rider.location
    except RiderLocation.DoesNotExist:
        return JsonResponse({"error": "Location not available yet"}, status=404)

    return JsonResponse({
        "latitude": str(location.latitude),
        "longitude": str(location.longitude),
        "updated_at": location.updated_at.isoformat(),
    })  