import datetime
import calendar
from django.db.models import Q, Avg, Count
from django.db.models import Count, Min, Max, Sum, Avg
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from digitalmarket.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView

from .forms import NewSellerForm
from .models import SellerAccount
from sellers.mixins import SellerAccountMixin

from billing.models import Transaction
from products.models import Product
from braces import views

import datetime
from django.utils import timezone
from pytz import timezone




class SellerProductDetailRedirectView(RedirectView):
    permanent=True

    def get_redirect_url(self, *args, **kwargs):
        obj=get_object_or_404(Product, pk=kwargs['pk'])
        return obj.get_absolute_url()



class SellerTransactionListView(SellerAccountMixin, ListView):
    model=Transaction
    template_name="sellers/transaction_list_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['special'] = 'background-color: linen;'
        return context



class SellerDashboard(SellerAccountMixin, FormMixin, View):
    form_class = NewSellerForm
    success_url = "/seller"


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            self.form_invalid(form)


    def get(self, request, *args, **kwargs):
        apply_form = self.get_form()
        account = self.get_account()
        exists = account
        active = None
        context = {}

        if exists:
            active =  account.active

        if exists and active:
            context["title"] = "My Sales"
            context["products"] = self.get_products()
            transactions_today = self.get_transactions_today()
            context["transactions_today"] = transactions_today
            context["today_sales"] = self.get_today_sales()
            context["total_sales"] = self.get_total_sales()
            context["transactions"] = self.get_transactions().exclude(id__in=transactions_today)
        elif exists and not active:
            context["title"] = "Please contact Site Admin."
            # !!!!!!!!!!!!!!

        elif not exists and not active:
            context["title"] = "Apply for Account"
            context["apply_form"] = apply_form
        else:
            pass

        return render(request, "sellers/dashboard.html", context )




    def form_valid(self, form):
        valid_data = super().form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data





    def get_transactions_today(self):
        today = datetime.date.today()
        today_min = datetime.datetime.combine(today, datetime.time.min)
        today_max = datetime.datetime.combine(today, datetime.time.max)
        today_min = today_min.replace(tzinfo=timezone('UTC'))
        today_max = today_max.replace(tzinfo=timezone('UTC'))

        return self.get_transactions().filter(timestamp__range=(today_min, today_max))





    def get_total_sales(self):
        transactions = self.get_transactions().aggregate(Sum("price"))
        total_sales = transactions["price__sum"]
        return total_sales




    def get_today_sales(self):
        transactions = self.get_transactions_today().aggregate(Sum("price"))
        total_sales = transactions["price__sum"]
        return total_sales




    def get_total_average_sales(self):
        transactions = self.get_transactions_today().aggregate(Avg("price"))
        total_sales = transactions["price__avg"]
        return total_sales




    def get_total_and_average_of_sales(self):
        transactions = self.get_transactions_today().aggregate(Sum("price"), Avg("price"))
        return transactions
