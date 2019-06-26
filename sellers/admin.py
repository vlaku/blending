from django.contrib import admin
from .models import SellerAccount

class SellerAccountAdmin(admin.ModelAdmin):
    list_display = ["__str__", "active"]

admin.site.register(SellerAccount, SellerAccountAdmin)