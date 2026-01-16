from django.contrib.auth import login

from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy

from django.views import generic

from ..forms import RegistrationForm

class UserLoginView(LoginView):
    template_name = "core/registration/login.html"

class UserRegistrationView(generic.CreateView):
    form_class = RegistrationForm
    template_name = "core/registration/register.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
