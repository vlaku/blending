from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.urls import reverse

from products.models import Product



class TagQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class TagManager(models.Manager):
	def get_queryset(self):
		return TagQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return super().all(*args, **kwargs).active()


class Tag(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True, blank=True)
	products = models.ManyToManyField(Product, blank=True)
	active = models.BooleanField(default=True)

	objects = TagManager()


	def __str__(self):
		return str(self.title)


	def get_absolute_url(self):
		view_name = "tags:detail"
		return reverse(view_name, kwargs={"slug":self.slug})



def tag_pre_save_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)
	print(instance.slug)
pre_save.connect(tag_pre_save_receiver, sender=Tag)
