from django.views import generic

from ..models import Category

class CategoryIndexView(generic.ListView):
    template_name = "core/category/index.html"
    context_object_name = "category_list"

    def get_queryset(self):
        return Category.objects.all()

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "core/category/detail.html"