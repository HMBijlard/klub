from django.urls import include, path

from . import views

app_name = 'core'

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("categories/", views.CategoryIndexView.as_view(), name="category-index"),
    path("categories/<int:pk>", views.CategoryDetailView.as_view(), name="category-detail"),
    path("products/", views.ProductIndexView.as_view(), name="product-index"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/offer/", views.ProductCreateOfferView.as_view(), name="product-offer"),
    path("accounts/register/", views.UserRegistrationView.as_view(), name="register"),
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("wishlist/", views.WishlistView.as_view(), name="wishlist-index"),
    path("wishlist/add/<int:product_id>", views.WishlistToggleView.as_view(), name="wishlist-toggle"),
    path("profile/<int:pk>", views.SellerProfileView.as_view(), name="profile"),
    path("profile/edit/", views.SellerProfileUpdateView.as_view(), name="profile-edit"),
    path("cart/add/", views.CartAdd.as_view(), name="cart-add"),
]
