from django.contrib import admin

from analytics.models import TagView

class TagViewAdmin(admin.ModelAdmin):
	list_display = ["user", "tag", "count"]
	search_fields = ["tag", "user"]
	


admin.site.register(TagView, TagViewAdmin) 