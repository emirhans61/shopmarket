from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    """A completed order placed by a user."""

    STATUS_CHOICES = [
        ("pending",    "Pending"),
        ("processing", "Processing"),
        ("shipped",    "Shipped"),
        ("delivered",  "Delivered"),
        ("cancelled",  "Cancelled"),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shipping details
    full_name   = models.CharField(max_length=200)
    address     = models.TextField()
    city        = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone       = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

    def get_total(self):
        """Sum of all order item subtotals."""
        return sum(item.get_subtotal() for item in self.items.all())


class OrderItem(models.Model):
    """
    A single product line within an order.
    Price is stored here so order history stays accurate
    even if the product price changes later.
    """
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.price * self.quantity