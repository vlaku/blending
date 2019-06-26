from django.conf import settings
from django.db import models
from products.models import Product

'''
buyer's transaction
user (=buyer) purchases from seller (Product.seller)
'''
class Transaction(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	product =models.ForeignKey(Product, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=7, decimal_places=2, default=9.99, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	success = models.BooleanField(default=True)

	def __str__(self):
		return "%s" %(self.id)

	class Meta:
		ordering = ['-timestamp']
