
from django import forms
from django.forms import TextInput
from products.models import Product


from products.models import *
from sellers.models import SellerAccount
from .mixins import DashboardSearchMixin
from django.db.models import Q, Avg, Count





class SearchForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=['title', 'description']
        widgets = {'name' : TextInput(attrs={'class' : 'input',
                                             'placeholder' : 'Product',
                                             })}
