from django.http import HttpResponseBadRequest, HttpResponseNotFound

from django.shortcuts import redirect

from django.views import View

from ..forms import CartAddForm

from ..models import Product


class CartAdd(View):
    def post(self, request, *args, **kwargs):
        form = CartAddForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Invalid input")
        product_id = form.cleaned_data["product_id"]
        if not Product.objects.filter(pk=product_id).exists():
            return HttpResponseNotFound(f"Product with id { product_id} does not exist")
        quantity = form.cleaned_data["quantity"]

        cart = request.session.get("cart", {})

        product_id = str(product_id)

        cart[product_id] = quantity

        request.session["cart"] = cart

        return redirect("core:product-detail", pk=product_id)


        
        
