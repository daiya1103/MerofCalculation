from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm
from .models import Product, Seller, SellerProduct, ProductKey
from user.models import User, UserProperty

class UserPropertyInline(admin.StackedInline):
    model = UserProperty
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines= (UserPropertyInline,)
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),
        (None, {
            'fields': (
                'date_joined',
                'username',
                'is_active',
                'is_admin',
            )
        })
    )
    list_display = ('username', 'is_active')
    list_filter = ()
    ordering = ()
    filter_horizontal = ()

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password',),
        }),
    )

    add_form = UserCreationForm

admin.site.register(User, CustomUserAdmin)
admin.site.register(Seller)
admin.site.register(SellerProduct)
admin.site.register(Product)
admin.site.register(ProductKey)