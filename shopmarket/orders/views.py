from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    """
    Checkout page — shows the cart summary and a shipping form.
    On POST: creates the Order and OrderItems, then clears the cart.
    """
    # Get the user's cart — redirect if empty
    try:
        cart  = Cart.objects.get(user=request.user)
        items = cart.items.select_related("product").all()
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty.")
        return redirect("products:list")

    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("products:list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the order
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Create order items from cart items
            for cart_item in items:
                OrderItem.objects.create(
                    order    = order,
                    product  = cart_item.product,
                    quantity = cart_item.quantity,
                    price    = cart_item.product.price,  # snapshot price
                )
                # Reduce stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()

            # Clear the cart
            cart.items.all().delete()

            messages.success(request, f"Order #{order.pk} placed successfully!")
            return redirect("orders:detail", pk=order.pk)
    else:
        form = CheckoutForm()

    context = {
        "form":  form,
        "cart":  cart,
        "items": items,
    }
    return render(request, "orders/checkout.html", context)


@login_required
def order_list(request):
    """Show all orders placed by the current user."""
    orders = request.user.orders.all()
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    """Show details of a single order."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})