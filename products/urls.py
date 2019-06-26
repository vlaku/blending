from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, path
from django.views.generic.base import RedirectView

from django.conf.urls.static import static
from django.contrib import admin
from . import views
from .views import *
# (
#     ProductCreateView,
#     ProductDeleteView,
#     ProductDetailView,
#     ProductDownloadView,
#     ProductListView,
#     ProductUpdateView,
#     ProductRatingAjaxView,
#     VendorListView,
#     CuratedProducts_ListView,
#     )
#

app_name="products"

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('curated/<slug>/', CuratedProductsListView.as_view(), name='curated_list'),
    path('ajax/rating/', ProductRatingAjaxView.as_view(), name='ajax_rating'),
    ## session check:
    path('all', articles, name='articles'),
    path('get/<int:pk>', article, name='article'),
    path('language/<language>/', language),
    # /products/language/en-us/
    # /products/language/pl/
    path('vendor/', RedirectView.as_view(pattern_name='products:list'), name='vendor_list'),
    path('vendor/<vendor_name>/', VendorListView.as_view(), name='vendor_detail'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('<slug>/', ProductDetailView.as_view(), name='detail_slug'),
    path('<int:pk>/download/', ProductDownloadView.as_view(), name='download'),
    path('<slug>/download/', ProductDownloadView.as_view(), name='download_slug'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='update'),
    path('<slug>/edit/', ProductUpdateView.as_view(), name='update_slug'),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
