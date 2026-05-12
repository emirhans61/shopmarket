# ShopMarket — Django Term Project

A full-featured online marketplace built with Django.

## Features

- Browse and search products by name or category
- Filter products by category pills
- User authentication (login, signup, logout)
- AJAX-powered shopping cart (no page reload)
- Order checkout and order history
- Admin panel for managing products, categories, and orders

## Tech Stack

- Python 3.11 / Django 4.2
- SQLite (development database)
- Bootstrap 5 + Bootstrap Icons
- Vanilla JS (AJAX cart)

## Setup Instructions

### 1. Clone and create virtual environment

```bash
git clone <your-repo-url>
cd shopmarket
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install django pillow
```

> `pillow` is required for the `ImageField` on Product.

### 3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 — the shop is live.
Admin panel: http://127.0.0.1:8000/admin

### 6. Add sample data

Go to the admin panel and:
1. Create some **Categories** (e.g. Electronics, Clothing, Books)
2. Create some **Products** under those categories

## Project Structure

```
shopmarket/
├── shopmarket/          # Project config (settings, urls)
├── templates/           # Global templates (base.html)
├── products/            # Product listing, search, detail
├── accounts/            # Login, signup, logout
├── cart/                # AJAX cart
├── orders/              # Checkout and order history
└── media/               # Uploaded product images
```

## Architecture & Design Notes

- **products/models.py** — `Category` and `Product` models; Product has a ForeignKey to Category
- **cart/models.py** — `Cart` (OneToOne with User) and `CartItem` (FK to Cart and Product)
- **orders/models.py** — `Order` and `OrderItem`; price is stored on OrderItem to preserve history
- **cart/context_processors.py** — injects `cart_count` into every template for the navbar badge
- AJAX cart uses `fetch()` + Django JSON views + CSRF token for seamless add-to-cart

## Deployment (PythonAnywhere)

1. Upload project via Git or zip upload
2. Create a web app → manual config → Django
3. Set `WSGI_APPLICATION` path, virtualenv path
4. Run `python manage.py collectstatic`
5. Set `DEBUG = False` and `ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']` in settings
