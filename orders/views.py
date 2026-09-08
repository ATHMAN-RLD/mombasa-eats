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

from django.contrib import messages
from restaurants.models import Restaurant
from .models import Order, OrderItem


def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("view_cart")

    cart_items = []
    total = 0
    restaurant = None
    for item_id_str, quantity in cart.items():
        menu_item = get_object_or_404(MenuItem, id=int(item_id_str))
        restaurant = menu_item.restaurant
        subtotal = menu_item.price * quantity
        total += subtotal
        cart_items.append({"item": menu_item, "quantity": quantity, "subtotal": subtotal})

    if request.method == "POST":
        order = Order.objects.create(
            restaurant=restaurant,
            customer_name=request.POST.get("customer_name"),
            customer_phone=request.POST.get("customer_phone"),
            delivery_address=request.POST.get("delivery_address"),
            total_amount=total,
        )
        for entry in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=entry["item"],
                item_name=entry["item"].name,
                price=entry["item"].price,
                quantity=entry["quantity"],
            )

        from django.conf import settings as django_settings
        from payments.mpesa import initiate_stk_push, format_phone_number
        from payments.models import MpesaTransaction 

        stk_response = initiate_stk_push(
            
            phone_number=format_phone_number(request.POST.get("customer_phone")),
            amount=total,
            account_reference=f"Order{order.id}",
            callback_url=django_settings.MPESA_CALLBACK_URL,
        )

        MpesaTransaction.objects.create(
            order=order,
            checkout_request_id=stk_response["CheckoutRequestID"],
            merchant_request_id=stk_response["MerchantRequestID"],
            phone_number=request.POST.get("customer_phone"),
            amount=total,
        )

        request.session["cart"] = {}
        request.session.modified = True
        return redirect("order_confirmation", order_id=order.id) 

    return render(request, "orders/checkout.html", {"cart_items": cart_items, "total": total})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_confirmation.html", {"order": order})   