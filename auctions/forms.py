from django import forms


class CreateListing(forms.Form):
    CHOICES = [
        ("", "Select a category"),
        ("fashion", "Fashion"),
        ("toys", "Toys"),
        ("electronics", "Electronics"),
        ("home", "Home"),
    ]

    item_name = forms.CharField(
        label="Item Name",
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter title here..."}
        ),
    )
    image_url = forms.URLField(
        label="Item Image URL",
        max_length=255,
        required=False,
        widget=forms.URLInput(
            attrs={"class": "form-control", "placeholder": "Enter image URL here..."}
        ),
    )
    starting_price = forms.DecimalField(
        label="Starting price",
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter starting bid here..."}
        ),
    )
    category = forms.ChoiceField(
        label="Category",
        choices=CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter description here...",
                "rows": 5,
                "cols": 100,
            }
        )
    )
