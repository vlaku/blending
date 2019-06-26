import calendar
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from json_response import JsonResponse
from django.views.generic import View

from digitalmarket.mixins import AjaxRequiredMixin

from products.models import Product, MyProducts
from billing.models import Transaction
from braces import views




class CheckoutAjaxView(AjaxRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if not (request.user.is_authenticated):
            return JsonResponse({}, status=401)

        user=request.user

        product_id = request.POST.get("product_id")   ##przejete z ajaxa na stonie product_detail.html na ktora wyrzuca ten View

        exists = Product.objects.filter(id=product_id).exists()
        if not exists:
            return JsonResponse({},status=404)

        product_obj = Product.objects.filter(id=product_id).first()
        #na wypadek gdyby byl inny produkt o takim samym id; mozna tez tak:
        # try:
        #   product_obj = Product.objects.filter(id=product_id)
        # except:
        #   product_obj = Product.objects.filter(id=product_id).first()


        # credit card required **

        # run transaction:
        trans_obj = Transaction.objects.create(
            user=request.user,
            product= product_obj,
            price=product_obj.get_price)


        my_products = MyProducts.objects.get_or_create(user=request.user)[0]
        my_products.products.add(product_obj)

        download_link = product_obj.get_download()
        preview_link = download_link + "?preview=True"

        data = {
        "download":download_link,
        "preview":preview_link,
        }
                # data = {
        # "works":True,
        # "time":datetime.datetime.now(),
        # }
        return JsonResponse(data)  #python 'data' converted into JSON (w test.html widac, http://127.0.0.1:8000/test/)







class CheckoutTestView(View):


    def post(self, request, *args, **kwargs):
        # print(request.POST)
        print(request.POST.get("testData"))  # przychwytuje zmienna ze slownika json o nazwie data z jQuery w dashboard/test.html
        # below is python dictionary, not json
        if request.is_ajax():
            if not (request.user.is_authenticated):
                data = {
                    "works":False,
                }
                return JsonResponse(data, status=401)
        # data nizej to data wywolywane przez jquery w dashboard/test.html:
        #    	request.done(function(data){
        #    		if (data.works){
            data = {
                "works":True,
                "time":"%s <br> %s" %("Super, drukuje",datetime.datetime.now()),
            }
            return JsonResponse(data)  #python 'data' is being changed
            # into JSON  (i w test.html widac to)
            ## dzieki czemu kontekst slownikowy data wyzej
            ## bedzie odczytany przez jquery w checkout/text.html
            ##  data.time i data.works
        return HttpResponse('Checkout Test View Here!')



    def get(self, request, *args, **kwargs):
        #return HttpResponse('Checkout Test View Here!')
        template = "checkout/test.html"
        context = {}
        return render(request, template, context)







def kalendarz(request):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    # calendar_text = calendar.TextCalendar(calendar.SUNDAY)
    calendar1 = calendar.HTMLCalendar(calendar.MONDAY)
    CAL = calendar1.formatmonth(year, month)
    CAL_p = calendar1.formatmonth(year, month-1)
    CAL_f = calendar1.formatmonth(year, month+1)
    context = {
        'CAL_p':CAL_p,
        'CAL':CAL,
        'CAL_f':CAL_f
    }

    ## return musi byc na calkowicie pusta strone
    ## nie moze byc na strone, na ktora daje wyrzut juz jakis view
    return render(request, 'calendar.html', context )
    # wywolac w calendar.html:  {{CAL|safe}}
    # wlaczac w inne html jak nizej:
    # <embed type="text/html" width=100% height=30%  class="kalendarz" style="overflow: hidden;" src="{% url 'blog:kalendarz' %}" />
