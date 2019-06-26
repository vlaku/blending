
from django.db.models import Q, Avg, Count
from products.models import *
from sellers.models import SellerAccount


class DashboardSearchMixin(object):
    account = None
    products = []
    transactions = []

    def get_account(self):
        user = self.request.user
        accounts = SellerAccount.objects.filter(user=user)

        if accounts.exists() and accounts.count() == 1:
            self.account = accounts.first()
            return accounts.first()
        return None



    def get_products(self):
        account = self.get_account()
        products = Product.objects.filter(seller=account)
        self.products = products
        return products



    def get_curated(self):
        curated = CuratedProducts.objects.all()

        return curated


    ## search-bar
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs) 
        qs = self.get_products()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
                )
        return qs
