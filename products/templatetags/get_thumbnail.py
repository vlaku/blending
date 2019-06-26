from django import template
from products.models import Product, THUMB_CHOICES


register = template.Library()

@register.filter
def get_thumbnail(obj, arg):
	'''
	obj==Product.instance

	get_thumbnail(p, 'micro')

	w template:
	<img src="{{ instance|get_thumbnail:'micro' }}"/>

	'''
	arg = arg.lower()
	if not isinstance(obj, Product):
		raise TypeError("This is not a valid Product model.")

	choices = dict(THUMB_CHOICES)
	if not choices.get(arg):
		raise TypeError("This is not a valid argument type for the product model.")
	try:
		return obj.thumbnail_set.filter(type=arg).first().media.url
	except:
		return None
