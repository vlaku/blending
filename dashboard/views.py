import random
from django.shortcuts import render
from django.views.generic import View
from products.models import *
from sellers.models import SellerAccount
from .mixins import DashboardSearchMixin
from django.db.models import Q, Avg, Count
from braces import views

import json
from collections import OrderedDict
from django.http import HttpResponse
from .forms import SearchForm



class DashboardView(DashboardSearchMixin, View):
    template_name="dashboard/view.html"


    def get(self, request, *args, **kwargs):
        tag_views = None
        products = None
        sug_products = None
        top_tags = None

    #     curated = CuratedProducts.objects.filter(active=True).order_by("?")[:3]
    #     try:
    #         tag_views = request.user.tagview_set.all().order_by("-count")
    #     except:
    #         pass

    #     owned = None
    #     try:
    #         owned = request.user.myproducts.products.all()
    #     except:
    #         pass

    #     account=None
    #     try:
    #         account = SellerAccount.objects.filter(user=request.user).first()
    #     except:
    #         print(SellerAccount.objects.filter(user=request.user), "    dashboard views")

    #     my_forsale_prods = None
    #     try:
    #         my_forsale_prods = Product.objects.filter(seller=account)
    #     except:
    #         pass



    #     if tag_views:
    #         top_tags = [x.tag for x in tag_views]
    #         top_tags = sorted(top_tags, key=lambda x: random.random())
    #         sug_products = Product.objects.all()
    #         if my_forsale_prods:
    #             sug_products = sug_products.exclude(seller=account)

    #         if owned:
    #             sug_products = sug_products.exclude(pk__in=owned)

    #         filtered = sug_products.filter(tag__in=top_tags)
    #         if filtered.count() < 10:
    #             pass
    #         else:
    #             sug_products = filtered


    #         if sug_products.count() < 8:
    #             sug_products = sug_products.order_by("?")
    #         else:
    #             sug_products= sug_products.distinct()[:11]
    #             sug_products= sorted(sug_products, key = lambda x: random.random())



    #     favourite = []
    
    #     if request.user.is_authenticated:
    #         user=request.user

    #         data_list = [] 

    #         if user.tagview_set.count() > 0:
    #             for q in user.tagview_set.all():
    #                 data_list.append(q.count)

    #         new_list = []

    #         while data_list:
    #             maximum = data_list[0]  # arbitrary number in list 
    #             for x in data_list: 
    #                 if x > maximum:
    #                     maximum = x
    #             new_list.append(maximum)
    #             data_list.remove(maximum)    

    #         ## tylko najpopularniejsze:
    #         if len(new_list)>0:
    #             new_list = new_list[:7]
    #             for item in new_list:
    #                 tt = user.tagview_set.filter(count=item)[0]
    #                 # print(item, tt)
    #                 favourite.append(tt)


    #     context = {
    #         "top_tags":top_tags,
    #         "curated":curated,
    #         "sug_products":sug_products,
    #         "favourite":favourite
    #     }
        # return render(request, "dashboard/view.html", context )

        context = {}     
        return render(request, "dashboard/view.html", context )





def render_json_response(request, data, status=None):
    """response を JSON で返却"""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    callback = request.GET.get('callback')
    if not callback:
        callback = request.POST.get('callback')
    if callback:
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=status)
    else:
        response = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
    return response




def json_list(request):
    data = {}
    file = 'sellers_and_buyers_stock.json'
    data['selling'] = []
    data['buying'] = []

    uzytkown = SellerAccount.objects.select_related('user').all()
    buyers = []
    uniques = []
    sellerzy = []

    sellers= []

    for pps in Thumbnail.objects.select_related("product").all():
        if pps.product.description not in uniques:
            uniques.append(pps.product.description)
            sells = str(pps.product.seller)
            sellerzy.append(sells)
            what = str(pps.product.description)
            data['selling'].append({sells: what, })

            sellers_dict = OrderedDict([
                ('seller', sells),
                ('product', what),
            ])
            sellers.append(sellers_dict )


    for one in uzytkown:
        who = str(one.user)
        if who in sellerzy:
            how_many = one.user.myproducts
            for x in one.user.myproducts.products.all():
                what = str(x)
                data['buying'].append({who: what})
                buyers_dict = OrderedDict([
                    ('who', who),
                    ('product', what),
                    ('sellers', sellers)
                ])
                buyers.append(buyers_dict)



    with open(file, 'w') as outfile:
        json.dump(data, outfile)

    return render_json_response(request, data)
