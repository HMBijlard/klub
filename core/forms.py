from django import forms

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError

from .models import Product, ProductOffering, UserRole

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

        UserRole.objects.create(
            user=user,
            role=self.cleaned_data["role"],
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
