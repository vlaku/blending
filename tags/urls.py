from django.conf import settings
from django.conf.urls import url  #include, 
from django.conf.urls.static import static
from django.urls import include, path 
from . import views 
from .views import TagDetailView, TagListView 


app_name="tags"

urlpatterns = [
    path('', TagListView.as_view(), name='list'),   # tag_list.html
    path('<int:pk>/', TagDetailView.as_view(), name='detail'),  # tag_detail.html
    path('<slug>/', TagDetailView.as_view(), name='detail_slug'),  # tag_detail.html
] 

