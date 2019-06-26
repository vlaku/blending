from django.conf import settings
#from django.conf.urls import url  #include, 
from django.urls import include, path 

from . import views 
from .views import (    SellerDashboard, SellerTransactionListView, SellerProductDetailRedirectView  )
from products.views import SellerProductListView, ProductUpdateView, ProductCreateView  #, create_view




app_name="sellers"

urlpatterns = [
    path('', SellerDashboard.as_view(), name='dashboard'),   
    path('products/add/', ProductCreateView.as_view(), name='product_create'),  # form.html    sellers:product_create
    #path('products/add/', create_view, name='product_create'),  # form.html    sellers:product_create
    path('products/', SellerProductListView.as_view(), name='product_list'),  # sellers/product_list_view.html   sellers:product_list
    path('products/<int:pk>/', SellerProductDetailRedirectView.as_view()), 
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'), 
    path('transactions/', SellerTransactionListView.as_view(), name='transactions'), 
] 
# SellerProductDetailRedirectView