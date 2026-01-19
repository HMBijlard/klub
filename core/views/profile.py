import json

from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse, reverse_lazy

from django.views import generic

from ..forms import SellerProfileForm

from ..models import SellerProfile

from ..mixinz import SellerRequiredMixin

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
    
class SellerProfileUpdateView(LoginRequiredMixin, SellerRequiredMixin, generic.UpdateView):
    form_class = SellerProfileForm
    template_name = "core/profile/edit.html"

    def get_object(self, queryset=None):
        profile, _ = SellerProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_success_url(self):
        return reverse(
            "core:profile",
            kwargs={"pk": self.object.user.pk}
        )
