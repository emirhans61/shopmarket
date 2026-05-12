from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    """
    Main shop page.
    Supports:
      - ?q=<search term>  — searches name and description
      - ?category=<slug>  — filters by category
    """
    products   = Product.objects.select_related("category").all()
    categories = Category.objects.all()

    query    = request.GET.get("q", "").strip()
    cat_slug = request.GET.get("category", "").strip()

    # Search filter
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Category filter
    active_category = None
    if cat_slug:
        active_category = get_object_or_404(Category, slug=cat_slug)
        products = products.filter(category=active_category)

    context = {
        "products":        products,
        "categories":      categories,
        "query":           query,
        "active_category": active_category,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, pk):
    """Single product detail page."""
    product = get_object_or_404(Product, pk=pk)
    # Related products from the same category (excluding this one)
    related = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk)[:4]

    context = {
        "product": product,
        "related": related,
    }
    return render(request, "products/product_detail.html", context)
