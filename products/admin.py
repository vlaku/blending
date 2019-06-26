from django.contrib import admin
from .models import Product, MyProducts, Thumbnail, ProductRating, CuratedProducts


# there must be a ForeignKey realtion between Thumbnail and Product to do TabularInline
class ThumbnailInline(admin.TabularInline):
    extra = 1  #only 1 space extra
    model = Thumbnail



class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline]
    list_display = ["__str__", "seller", "description", "price", "sale_price"]
    search_fields = ["title", "description"]
    list_filter=["sale_price"]
    list_editable=["sale_price"]
# prepopulated_fields = {"slug": ("title",)}  #pokaze slug z automatu

    class Meta:
        model=Product


admin.site.register(Product, ProductAdmin)
admin.site.register(Thumbnail)


class MyProductsAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user"]

admin.site.register(MyProducts, MyProductsAdmin)




class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ["__str__", "product", "user", "verified"]

admin.site.register(ProductRating, ProductRatingAdmin)
admin.site.register(CuratedProducts)
