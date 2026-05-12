from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignupForm


def signup_view(request):
    """Register a new user account."""
    if request.user.is_authenticated:
        return redirect("products:list")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # log in automatically after signup
            messages.success(request, f"Welcome, {user.username}! Your account was created.")
            return redirect("products:list")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    """Log in an existing user."""
    if request.user.is_authenticated:
        return redirect("products:list")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            # Go to the page they were trying to visit, or home
            next_url = request.GET.get("next", "products:list")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        # Add Bootstrap classes
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("products:list")
