from django import forms

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError

from django.contrib.gis import forms as gis_forms

from .models import Product, ProductOffering, UserRole, SellerProfile

User = get_user_model()

class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserRole.Role.choices,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = User
        fields = ("username",)

    def save(self, commit=True):
        user = super().save(commit)

        role = self.cleaned_data["role"]

        UserRole.objects.create(
            user=user,
            role=role,
        )

        if role == UserRole.Role.SELLER:
            SellerProfile.objects.create(
                user=user
            )

        return user
    
class ProductOfferingForm(forms.ModelForm):
    min_quantity = forms.IntegerField(min_value=1)
    discount = forms.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = Product
        fields = ["name", "categories", "description"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        return super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        offering = ProductOffering(
            min_quantity=cleaned.get("min_quantity"),
            discount=cleaned.get("discount"),
            seller=self.user,
        )

        try:
            offering.full_clean(exclude=["product"])
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for err in errors:
                    self.add_error(field if field in self.fields else None, err)
        return cleaned

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ["description", "locations"]
        widgets = {
            "locations": gis_forms.OSMWidget(attrs={
                "map_width": 800,
                "map_height": 500,
            })
        }
