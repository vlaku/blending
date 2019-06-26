from django.contrib import admin
from .models import Transaction

class BillingAdmin(admin.ModelAdmin):
	list_display = ["__str__", "user", "product"]

admin.site.register(Transaction, BillingAdmin)
