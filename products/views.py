import os
import io
import json
from wsgiref.util import FileWrapper
from django.core.files.base import ContentFile, File
#   from django.core.servers.basehttp import FileWrapper   #stare django
from mimetypes import guess_type

from django.db.models import Q, Avg, Count

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import Http404, HttpResponse
from json_response import JsonResponse

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View

from django.utils import timezone

from analytics.models import TagView
from digitalmarket.mixins import (
    AjaxRequiredMixin,
    MultiSlugMixin,
    SubmitBtnMixin,
    LoginRequiredMixin,
    StaffRequiredMixin,
    )

from products.forms import ProductAddForm, ProductModelForm
from products.models import Product, ProductRating, MyProducts, CuratedProducts
from products.mixins import  ProductManagerMixin
from sellers.mixins import SellerAccountMixin
from sellers.models import SellerAccount

from tags.models import Tag
from django.core.files.storage import FileSystemStorage
from braces import views


class ProductRatingAjaxView(AjaxRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        if not (request.user.is_authenticated):
            return JsonResponse({}, status=401)

        user=request.user
        product_id = request.POST.get("product_id")
        rating_value = request.POST.get("rating_value")

        exists = Product.objects.filter(id=product_id).exists()
        if not exists:
            return JsonResponse({},status=404)

        product_obj = Product.objects.filter(id=product_id).first()

        rating_obj, rating_obj_created = ProductRating.objects.get_or_create(user=user, product=product_obj)
        try:
            rating_obj = ProductRating.objects.get(user=user, product=product_obj)
        except ProductRating.MultipleObjectsReturned:
            rating_obj = ProductRating.objects.filter(user=user, product=product_obj).first()
        except:
            rating_obj = ProductRating()
            rating_obj.user = user
            rating_obj.product = product_obj
        rating_obj.rating = int(rating_value)

        try:
            myproducts = user.myproducts.products.all()
            if product_obj in myproducts:
                rating_obj.verified = True
            rating_obj.save()
        except:
            pass 


        data = { "success":True }
        return JsonResponse(data)



class ProductCreateView(SellerAccountMixin, SubmitBtnMixin, CreateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    submit_btn = "Add Product"


    def form_valid(self, form):
        seller = self.get_account()
        form.instance.seller = seller
        valid_data = super().form_valid(form)
        media = form.cleaned_data.get("media")

        tags = form.cleaned_data.get("tags")
        if tags:
            tags_list = tags.split(",")
            for tag in tags_list:
                if not tag == " ":
                    new_tag, created = Tag.objects.get_or_create(title=str(tag).strip())
                    new_tag.products.add(form.instance)

        return valid_data



class ProductDeleteView(SubmitBtnMixin, DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    form_class = ProductModelForm
    submit_btn = "Delete"

    def get_success_url(self):
        return reverse('sellers:product_list')



class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = Product
    form_class = ProductModelForm
    template_name = "form.html"
    submit_btn = "Update Product"

    def get_initial(self):
        initial = super().get_initial()
        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])
        return initial



    def form_valid(self, form):
        valid_data = super().form_valid(form)
        tags = form.cleaned_data.get("tags")
        obj = self.get_object()
        obj.tag_set.clear()
        if tags:
            tags_list = tags.split(",")
            for tag in tags_list:
                if not tag == " ":
                    new_tag, created = Tag.objects.get_or_create(title=str(tag).strip())
                    new_tag.products.add(self.get_object())
        return valid_data




class ProductDetailView(MultiSlugMixin, DetailView):
    model = Product


    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
                ).order_by("-pk")
        return qs



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = self.get_object()


        sa = SellerAccount.objects.filter(product=obj)[0]

        try:
            rating_obj = ProductRating.objects.filter(product=obj).exclude(user=sa.user)  ## ratingu sellera nie chcemy do sredniej itd.
            if rating_obj.exists():
                ocenki = {}
                username = 'username'
                ocenka = 'ocenka'
                procent_slupka = 'procent_slupka'
                ocenki['rating'] = []
                max_ocena = 5


                for one in rating_obj:
                    do_sredniej = one.rating
                    udzial = do_sredniej * 100 / max_ocena
                    udzial = '{:.0f}'.format(udzial)
                    ocenki['rating'].append({
                        username: str(one.user.username),
                        ocenka: str(one.rating),
                        procent_slupka: udzial,
                    })

            context["ocenki"] = ocenki['rating']


            rating_avg = rating_obj.aggregate(Avg("rating"), Count("rating"))
            context["rating_avg"] = rating_avg
        except:
            context["ocenki"] = []
            context["rating_avg"] = 0.0001


        tags = obj.tag_set.all()

        if self.request.user.is_authenticated:

            my_rating_obj = ProductRating.objects.filter(user=self.request.user, product=obj)
            if my_rating_obj.exists():
                context['my_rating'] = my_rating_obj.first().rating


            for tag in tags:
                new_view = TagView.objects.add_count(self.request.user, tag)
        return context






class ProductDownloadView(MultiSlugMixin, DetailView):
    model = Product
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj in request.user.myproducts.products.all():
            filepath = os.path.join(settings.MEDIA_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(open(filepath, encoding="utf8", errors='ignore'),10000) 
            mimetype = 'application/force-download'
            if guessed_type:
                mimetype = guessed_type
            response = HttpResponse(wrapper, content_type='mimetype')

            if not request.GET.get("preview"):
                response["Content-Disposition"] = "attachment; filename=%s"  %(obj.media.name)

            response["X-SendFile"] = str(obj.media.name)
            return response
        else:
            raise Http404



class ProductListView(ListView):
    model = Product
    template_name = "sellers/product_list_view.html"


    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
                ).order_by("-pk")
        return qs




class SellerProductListView(SellerAccountMixin, ListView):
    model = Product
    template_name = "sellers/product_list_view.html"


    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(seller=self.get_account())

        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
                ).order_by("-pk")
        return qs




# My Purchases 
class UserLibraryListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/library_list.html"

    def get_queryset(self, *args, **kwargs):
        obj = MyProducts.objects.get_or_create(user=self.request.user)[0]
        qs = obj.products.all()

        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
                )
        return qs





class VendorListView(ListView):
    model = Product
    template_name = "products/product_list.html"



    def get_object(self):
        vendor_name = self.kwargs.get("vendor_name")
        seller = get_object_or_404(SellerAccount, user__username=vendor_name)
        return seller



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["vendor_name"] = str(self.get_object().user.username)
        return context




    def get_queryset(self, *args, **kwargs):
        seller = self.get_object()
        qs = super().get_queryset(**kwargs).filter(seller=seller)

        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
                ).order_by("title")
        return qs







class CuratedProductsListView(ListView):
    model = CuratedProducts
    template_name = "products/curated_list.html"


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["object"] = str(self.get_object())

        update_section()
        usun_zbedne_sections()
        calosc = []
        for x in self.get_object().products.all():
            calosc.append(x)
        context["object_list"] = calosc
        return context



    def get_object(self):
        slug= self.kwargs.get("slug")
        this_curated_prod = get_object_or_404(CuratedProducts, slug=slug)
        return this_curated_prod


    def get_queryset(self, *args, **kwargs):
        this_curat = self.get_object()
        obj = super().get_queryset(**kwargs).filter(section_name=this_curat)[0]
        qs = obj.products.all()
        print(qs)


        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
                )
        print(qs)
        return qs





def update_section():
    for p in Product.objects.all():
        if not p.curatedproducts_set.all().exists():
            if p.tag_set.all().exists():
                for t in p.tag_set.all():
                    for cur in CuratedProducts.objects.filter(section_name__icontains=t):
                        cur.products.add(p)
    return CuratedProducts.objects.all()




def usun_zbedne_tagi():
    for t in Tag.objects.all():
        if t.products.all().count() == 0:
            t.delete()
    return Tag.objects.all()



def usun_zbedne_sections():
    for t in CuratedProducts.objects.all():
        if t.products.all().count() == 0:
            t.delete()
    return CuratedProducts.objects.all()







#############################################


def create_view(request):
    form = ProductModelForm(request.POST or None, request.FILES or None)


    if not form.is_valid():
        print('---FORM-NOT-VALID---')
        print(form.errors)
    else:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sale_price=instance.price
            instance.save()
            form.save()
        template="form.html"
        context={
            "form":form,
            "submit_btn":"Create Product",
            }
        return render(request, template, context)






def handle_uploaded_file(f):
    pass
    # sprawdz





def update_view(request, object_id=None):
    product = get_object_or_404(Product, id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if not form.is_valid():
        print('---FORM-NOT-VALID---')
        print(form.errors)
    else:
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
        template = "form.html"
        context = {
            "object":product,
            "form":form,
            "submit_btn":"Update Product",
            }
        return render(request, template, context)






def detail_slug_view(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        try:
            product = get_object_or_404(Product, slug=slug)
        except Product.MultipleObjectsReturned:
            product = Product.objects.filter(slug=slug).order_by("-title").first()
        except ValueError:
            raise Http404("No such page.")
        template = "detail_view.html"
        context = {
        "object":product,
        }
    else:
        template="not_found.html"
        context = { }
    return render(request, template, context)



def detail_view(request, object_id=None):
    if request.user.is_authenticated:
        try:
            product = get_object_or_404(Product, id=object_id)
        except ValueError:
            raise Http404("No such page.")
    template = "detail_view.html"
    context = {
        "object":product,
        }
    return render(request, template, context)


def list_view(request):
    queryset = Product.objects.all()
    template="products/list_view.html"
    context = {
    "queryset":queryset,
    }
    return render(request, template, context)





def wyrzuc_json(request):
    template="products/wyrzuc_json.html"

    dane = []
    with open('sellers_and_buyers_stock.json', 'r') as f:
        dane = json.load(f)
        f.close()

    context = {
    "dane":dane,
    }
    return render(request, template, context)






# def index(request):
#     queryset = Product.objects.all()
#     template="index.html"
#     context = {
#     "queryset":queryset,
#     }
#     return render(request, template, context)



def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'404.html', data)


def index(request):
    return HttpResponse("You're at the Home page of Django sample project error 404.")


################# sessions ######################


def articles(request):
    language = 'en-gb'
    session_language = 'en-gb'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    if 'lang' in request.session:
        session_language = request.session['lang']

    return render_to_response('articles.html',
                              {'articles': Product.objects.all(),
                              'language': language,
                              'session_language': session_language,
                               } )



def article(request, pk=1):
    return render_to_response('article.html',
                              {'article': Product.objects.get(id=pk)} )



def language(request, language='en-gb'):
    response = HttpResponse("setting language to %s" % language)
    response.set_cookie('lang', language)
    request.session['lang'] = language
    return response
