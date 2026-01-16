from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404, redirect

from django.views import generic, View

from django.urls import reverse

from ..models import Wishlist, Product

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
    template_name = "core/wishlist/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        wishlist, _ = Wishlist.objects.get_or_create(self.request.user)
        return wishlist.products.all()
    