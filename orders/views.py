from django.shortcuts import render, redirect, get_object_or_404
from restaurants.models import MenuItem


def add_to_cart(request, item_id):
    cart = request.session.get("cart", {})
    item_id_str = str(item_id)
    cart[item_id_str] = cart.get(item_id_str, 0) + 1
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("view_cart")


def view_cart(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0
    for item_id_str, quantity in cart.items():
        menu_item = get_object_or_404(MenuItem, id=int(item_id_str))
        subtotal = menu_item.price * quantity
        total += subtotal
        cart_items.append({"item": menu_item, "quantity": quantity, "subtotal": subtotal})
    return render(request, "orders/cart.html", {"cart_items": cart_items, "total": total})  