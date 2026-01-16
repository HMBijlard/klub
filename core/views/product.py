from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import transaction

from django.db.models import Count

from django.urls import reverse_lazy

from django.views import generic

from ..forms import ProductOfferForm

from ..models import Product, ProductOffering

class ProductIndexView(generic.ListView):
    template_name = "core/product/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.all()
    
class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "core/product/detail.html"

    def get_queryset(self):
        return super().get_queryset().annotate(wishlist_user_count=Count("wishlists__user", distinct=True))


class ProductCreateOfferView(LoginRequiredMixin, generic.CreateView):
    form_class = ProductOfferForm
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
