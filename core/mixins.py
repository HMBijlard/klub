from django.http import Http404

from .models import UserRole

class SellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, "userrole") or user.userrole.role != UserRole.Role.SELLER:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
