from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    """Shipping details form shown at checkout."""

    class Meta:
        model  = Order
        fields = ["full_name", "address", "city", "postal_code", "phone"]
        widgets = {
            "full_name":   forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}),
            "address":     forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Street address"}),
            "city":        forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Postal code"}),
            "phone":       forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number (optional)"}),
        }