from django.db import models
from django.conf import settings
from django.urls import reverse


class SellerAccount(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	managers_sellers=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_sellers", blank=True)
	active = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


	def __str__(self):
		return str(self.user.username)

	class Meta:
		ordering = ['-timestamp']


	def get_absolute_url(self):
		view_name = "products:vendor_detail"
		return reverse(view_name, kwargs={"vendor_name":self.user.username})
