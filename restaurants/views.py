
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Restaurant


def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, "restaurants/restaurant_list.html", {"restaurants": restaurants})


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
    menu_items = restaurant.menu_items.filter(is_available=True)
    return render(request, "restaurants/restaurant_detail.html", {
        "restaurant": restaurant,
        "menu_items": menu_items,
    })  