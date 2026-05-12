"""
Injects cart_count into every template automatically.
This powers the live cart badge in the navbar.
"""


def cart_count(request):
    """Return total item count for the logged-in user's cart."""
    count = 0
    if request.user.is_authenticated:
        try:
            from cart.models import Cart
            cart  = Cart.objects.get(user=request.user)
            count = cart.get_item_count()
        except Exception:
            count = 0
    return {"cart_count": count}
