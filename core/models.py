from django.conf import settings

from django.db import models

from django.core import validators

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=20)
    categories = models.ManyToManyField(
        Category,
        related_name="products",
        blank=True
    )
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class ProductOffering(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="seller",
    )
    min_quantity=models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1)
        ]
    )
    discount = models.SmallIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(100),
        ]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(min_quantity__gte=1),
                name="min_quantity_gte_1",
            ),
            models.CheckConstraint(
                condition=models.Q(discount__gte=1) & models.Q(discount__lte=100),
                name="discount_between_1_and_100",
            ),
        ]

    def __str__(self):
        return f"{self.product} offering by {self.seller}"

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product,
        related_name="wishlists",
    )

class UserRole(models.Model):
    class Role(models.TextChoices):
        CUSTOMER = ("customer", "Customer")
        SELLER = ("seller", "Seller")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)

    def __str__(self):
        return self.role.title()
    