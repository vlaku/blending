from django.http import Http404
from digitalmarket.mixins import (
	MultiSlugMixin,
	SubmitBtnMixin,
	LoginRequiredMixin,
	StaffRequiredMixin,
	)
from sellers.mixins import SellerAccountMixin



class ProductManagerMixin(SellerAccountMixin, object):
	def get_object(self, *args, **kwargs):
		seller=self.get_account()
		obj = super().get_object(*args, **kwargs)
		try:
			obj.seller == seller
		except:
			raise Http404("You might not be the owner of this product. Check products.mixins.ProductManagerMixin")

		if obj.seller == seller: 
			return obj

		else:
			raise Http404("You might not be the owner of this product. Check products.mixins.ProductManagerMixin")
