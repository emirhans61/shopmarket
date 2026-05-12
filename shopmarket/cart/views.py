import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    """Show all items currently in the user's cart."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items    = cart.items.select_related("product").all()

    context = {
        "cart":  cart,
        "items": items,
    }
    return render(request, "cart/cart_detail.html", context)


@login_required
def add_to_cart(request, product_id):
    """
    AJAX view — adds a product to the cart.
    Expects a POST request with optional JSON body: { "quantity": 2 }
    Returns JSON: { "success": true, "cart_total": 3 }
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required"}, status=405)

    product = get_object_or_404(Product, pk=product_id)

    # Read quantity from JSON body (default 1)
    quantity = 1
    try:
        body     = json.loads(request.body)
        quantity = int(body.get("quantity", 1))
    except (json.JSONDecodeError, TypeError):
        quantity = 1

    # Clamp quantity to available stock
    quantity = max(1, min(quantity, product.stock))

    # Get or create the cart for this user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Add item or increase quantity if already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity = min(cart_item.quantity + quantity, product.stock)
        cart_item.save()

    return JsonResponse({
        "success":    True,
        "cart_total": cart.get_item_count(),
        "message":    f"{product.name} added to cart!",
    })


@login_required
def remove_from_cart(request, item_id):
    """Remove a single CartItem from the cart."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart:detail")


@login_required
def update_cart(request, item_id):
    """Update the quantity of a CartItem."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)

    quantity = int(request.POST.get("quantity", 1))
    if quantity < 1:
        cart_item.delete()
        messages.info(request, "Item removed from cart.")
    else:
        cart_item.quantity = min(quantity, cart_item.product.stock)
        cart_item.save()
        messages.success(request, "Cart updated.")

    return redirect("cart:detail")
