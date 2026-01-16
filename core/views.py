import json

from django.contrib.auth import login, get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from django.db import transaction

from django.db.models import Count

from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy, reverse

from django.views import generic, View

from .forms import ProductOfferingForm, RegistrationForm, SellerProfileForm

from .models import Product, ProductOffering, Category, Wishlist, SellerProfile

from .mixinz import SellerRequiredMixin

class HomeView(generic.TemplateView):
    template_name = "core/home.html"

class CategoryIndexView(generic.ListView):
    template_name = "core/category_index.html"
    context_object_name = "category_list"

    def get_queryset(self):
        return Category.objects.all()

class ProductIndexView(generic.ListView):
    template_name = "core/product/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.all()
    
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "core/category_detail.html"

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "core/product/detail.html"

    def get_queryset(self):
        return super().get_queryset().annotate(wishlist_user_count=Count("wishlists__user", distinct=True))
    
class SellerProfileView(generic.DetailView):
    model = get_user_model()
    template_name = "core/profile/seller.html"
    context_object_name = "seller"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(profile__isnull=False)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        seller = ctx["seller"]

        points = seller.profile.locations

        geojson = None

        if points:
            points_4326 = points.clone()
            # technically redundant, as our data
            # is already in 4326 format
            points_4326.transform(4326)
            geojson = json.loads(points_4326.geojson) if points_4326.geojson else None
        ctx["locations_geojson"] = geojson
        return ctx


class UserRegistrationView(generic.CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class WishlistToggleView(View, LoginRequiredMixin):
    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

        if product in wishlist.products.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)

        next_url = request.POST.get("next") or reverse("product-detail", kwargs={"pk": product.id})

        return redirect(next_url)
    
class WishlistView(LoginRequiredMixin, generic.ListView):
    template_name = "core/wishlist_index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        wishlist, _ = Wishlist.objects.get_or_create(self.request.user)
        return wishlist.products.all()
    
class ProductOfferView(LoginRequiredMixin, generic.CreateView):
    form_class = ProductOfferingForm
    template_name = "core/product/offer.html"
    success_url = reverse_lazy("core:product-offer")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)

        ProductOffering.objects.create(
            product=self.object,
            seller=self.request.user,
            min_quantity=form.cleaned_data["min_quantity"],
            discount=form.cleaned_data["discount"],
        )

        messages.success(
            self.request,
            f"{self.object.name} added successfully!"
        )
        return response

class SellerProfileUpdateView(LoginRequiredMixin, SellerRequiredMixin, generic.UpdateView):
    form_class = SellerProfileForm
    template_name = "core/profile/edit.html"
    success_url = reverse_lazy("core:profile", kwargs={})

    def get_object(self, queryset=None):
        profile, _ = SellerProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_success_url(self):
        return reverse(
            "core:profile",
            kwargs={"pk": self.object.user.pk}
        )