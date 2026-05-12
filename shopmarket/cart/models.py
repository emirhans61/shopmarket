from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    """
    One cart per user (OneToOneField).
    Created automatically when user first adds an item.
    """
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        """Calculate total price of all items in the cart."""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        """Total number of individual items."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """A single product line inside a cart."""
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        """Price for this line (price × quantity)."""
        return self.product.price * self.quantity
