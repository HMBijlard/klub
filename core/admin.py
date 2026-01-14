from django.contrib import admin

from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Category, Product, UserRole

User = get_user_model()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

class UserRoleInline(admin.StackedInline):
    model = UserRole
    can_delete = False
    extra = 0

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "role":
            kwargs["choices"] = [
                ("customer", "Customer"),
                ("seller", "Seller"),
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

class UserAdmin(BaseUserAdmin):
    inlines = [UserRoleInline]
    list_display = BaseUserAdmin.list_display + ("get_role", )

    def get_role(self, object):
        try:
            return object.userrole.role.title()
        except UserRole.DoesNotExist:
            return "-"
    get_role.short_description = "Role"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)