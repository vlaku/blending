from django.conf import settings
from django.conf.urls import include
from django.urls import include, path
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

import products.views
from products.views import UserLibraryListView
import tags.views
import dashboard.views
from dashboard.views import DashboardView
import checkout.views
from checkout.views import CheckoutTestView, CheckoutAjaxView
import sellers.views
from accounts import views as accounts_views

from django.conf.urls import include, url

from django.views.generic import TemplateView

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# Debug Toolbar: 
if settings.DEBUG:
    import debug_toolbar


urlpatterns = [
    path('kwakwa/', admin.site.urls, name='admin'),
    # https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#hooking-adminsite-to-urlconf
    path('accounts/', include('accounts.urls')),
    path('', dashboard.views.DashboardView.as_view(), name='dashboard'),
    path('404', products.views.index, name='index'),
    path('checkout/', checkout.views.CheckoutAjaxView.as_view(), name='checkout'),
    path('library/', products.views.UserLibraryListView.as_view(), name='library'),
    path('products/', include('products.urls', namespace='products')),
    path('seller/', include('sellers.urls', namespace='sellers')),
    path('tags/', include('tags.urls', namespace='tags')),
    path('test/', checkout.views.CheckoutTestView.as_view(), name='test'),
]

handler404 = 'products.views.error_404_view'

urlpatterns += [
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'), ), name="favicon" ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]

if not settings.DEBUG:
    urlpatterns += [
        path('anymail/', include('anymail.urls')),  ## for sendgrid webhooks  # production only
    ]
