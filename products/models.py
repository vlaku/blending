import sys
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils.text import slugify
from django.urls import reverse
from sellers.models import SellerAccount

import os
import shutil
from PIL import Image
import random
from django.core.files import File


from django.db import IntegrityError
from django.shortcuts import render_to_response


from django.db import models
from django.db.models.signals import post_delete


User=settings.AUTH_USER_MODEL


def my_media_location(instance, filename):
    konc = ['png','jpg','jpeg','gif']
    try:
        name_ = filename.split('.')
        nazwa = instance.slug
        koncowka = name_[len(name_)-1]
        if koncowka in konc:
            nowanazwa = "%s.%s" % (nazwa, koncowka)
            return "%s/%s" % (instance.slug, nowanazwa)
        else:
            # print('We accept only png, jpg, jpeg and gif files')
            return 0
    except:
        # print('File is missing')
        return 0
        # reject the files 


# def download_media_location(instance, filename):
#     return "%s/%s" %(instance.slug, filename)


class Product(models.Model):
    seller=models.ForeignKey(SellerAccount, default=2, on_delete=models.CASCADE)
    media = models.ImageField(blank=True, null=True, upload_to=my_media_location)

    title = models.CharField(max_length=120)
    slug=models.SlugField(blank=True, unique=True)
    description = models.TextField(max_length=220)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=9.99, blank=True)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, default=9.99, blank=True)
    sale_active = models.BooleanField(default=False)

    def get_absolute_url(self):
        view_name = "products:detail_slug"
        return reverse(view_name, kwargs={"slug":self.slug})



    def get_edit_url(self):
        view_name = "sellers:product_edit"
        return reverse(view_name, kwargs={"pk":self.id})



    def __str__(self):
        return self.title


    def get_download(self):
        view_name = "products:download_slug"
        url = reverse(view_name, kwargs={"slug":self.slug})
        return url

    @property
    def get_price(self):
        if self.sale_price and self.sale_active:
            return self.sale_price
        return self.price



    def get_averrat(self):
        p = None
        one = 0
        rat = 0
        try:
            p = Product.objects.get(title=self)
            one = p.productrating_set.aggregate(Avg('rating'))
            rat = '{:.2f}'.format(one['rating__avg'])
        except:
            one = 0
            rat = 0
        return rat


    def get_html_price(self):
        price = self.get_price
        if price == self.sale_price:
            return self.price
        elif price < self.sale_price:
            return self.sale_price
        else:
            return " <span>%s</span> <span style='color: maroon; text-decoration: line-through;'>%s</span>" %(self.sale_price, self.price)



def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug




def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)



def create_new_thumb(media_path, instance, owner_slug, max_length, max_width):
    filename = os.path.basename(media_path)
    thumb = Image.open(media_path)
    size = (max_length, max_width)
    thumb.thumbnail(size, Image.ANTIALIAS)
    temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT, owner_slug)
    if not os.path.exists(temp_loc):
        os.makedirs(temp_loc)
    temp_file_path = os.path.join(temp_loc, filename)
    temp_image = open(temp_file_path, "wb")
    thumb.save(temp_image)
    thumb_data = open(temp_file_path, "r+b")  # 'rb+'
    thumb_file = File(thumb_data)

    instance.media.save(filename, thumb_file)
    shutil.rmtree(temp_loc, ignore_errors=True)
    return True



def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.media:
        try:
            hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
            sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
            micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')
            hd_max=(500,500)
            sd_max=(350,350)
            micro_max=(150,150)
            media_path = instance.media.path
            owner_slug = instance.slug
            if hd_created:
                try:
                    create_new_thumb(media_path, hd, owner_slug, hd_max[0], hd_max[1])
                except:
                    pass
            if sd_created:
                try:
                    create_new_thumb(media_path, sd, owner_slug, sd_max[0], sd_max[1])
                except:
                    pass
            if micro_created:
                try:
                    create_new_thumb(media_path, micro, owner_slug, micro_max[0], micro_max[1])
                except:
                    pass
        except:
            print('No media in Product instance')

post_save.connect(product_post_save_receiver, sender=Product)



###############################################
# https://djangosnippets.org/snippets/10638/
@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.media:
        if os.path.isfile(instance.media.path):
            os.remove(instance.media.path)

@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).media
    except sender.DoesNotExist:
        return False

    new_file = instance.media
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
###############################################













def thumbnail_location(instance, filename):
    name_ = filename.split('.')
    nazwa = instance.product.slug
    koncowka = name_[1]
    nowanazwa = "%s.%s" % (nazwa, koncowka)
    return "%s/%s" %(nazwa, nowanazwa)


THUMB_CHOICES=(
    ("hd","HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
    )


class Thumbnail(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)  ##this is the uploading user
    type = models.CharField(max_length=20, choices=THUMB_CHOICES, default='hd')
    height = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(
        height_field = "height",
        width_field = "width",
        blank=True, null=True,
        upload_to=thumbnail_location)

    def __str__(self):
        if self.media:
            return "%s" % (self.media.path)
        else:
            return "%s" %("empty")

    @property
    def image_url(self):
        if self.media and hasattr(self.media, 'url'):
            return self.media.url



##############################################
# https://djangosnippets.org/snippets/10638/
@receiver(models.signals.post_delete, sender=Thumbnail)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.media:
        if os.path.isfile(instance.media.path):
            os.remove(instance.media.path)

@receiver(models.signals.pre_save, sender=Thumbnail)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).media
    except sender.DoesNotExist:
        return False

    new_file = instance.media
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
##############################################








class MyProducts(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return "%s" %(self.products.count())


    class Meta:
        verbose_name = "My Products"
        verbose_name_plural = "My Products"







class ProductRating(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    rating=models.IntegerField(null=True, blank=True)
    verified=models.BooleanField(default=False)

    def __str__(self):
        return "%s" %(self.rating)


class CuratedProducts(models.Model):
    section_name = models.CharField(max_length=120)
    products = models.ManyToManyField(Product, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.section_name

    class Meta:
        verbose_name = "Curated products"
        verbose_name_plural = "Curated products"




def create_slug_curated(instance, new_slug=None):
    slug = slugify(instance.section_name)
    if new_slug is not None:
        slug = new_slug

    qs = CuratedProducts.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug



def curated_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug_curated(instance)

pre_save.connect(curated_pre_save_receiver, sender=CuratedProducts)







######################################### emails START #######
# This snippet goes somewhere inside your project,
# wherever you need to react to incoming emails.
import logging
from inbound_email.signals import email_received

def on_email_received(sender, **kwargs):
    """Handle inbound emails."""
    email = kwargs.pop('email')
    request = kwargs.pop('request')

    # your code goes here - save the email, respond to it, etc.
    logging.debug(
        "New email received from %s: %s",
        email.from_email,
        email.subject
    )

# pass dispatch_uid to prevent duplicates:
# https://docs.djangoproject.com/en/dev/topics/signals/
email_received.connect(on_email_received, dispatch_uid="something_unique")







from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from inbound_email.signals import email_received


def get_file(attachment):
    """Convert email.attachment tuple into a SimpleUploadedFile."""
    name, content, content_type = attachment
    return SimpleUploadedFile(name, content, content_type)


class Example(models.Model):
    """Example model that contains a FileField property."""
    file = models.FileField()


def on_email_received(sender, **kwargs):
    """Handle inbound emails."""
    email = kwargs.pop('email')
    for attachment in email.attachments:
        # we must convert attachment tuple into a file
        # before adding as the property.
        example = Example(file=get_file(attachment))
        example.save()