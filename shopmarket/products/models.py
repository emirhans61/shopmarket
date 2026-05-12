from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """A product category (e.g. Electronics, Clothing)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """A product listed in the shop."""
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    image       = models.ImageField(upload_to="products/", blank=True, null=True)
    category    = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0
