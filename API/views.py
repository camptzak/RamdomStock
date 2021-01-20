import socket
import yahoo_fin.stock_info as si

from math import isnan

from zinnia.models.entry import Entry

from django.views import View
from django.http import JsonResponse
from django_comments.models import Comment
# CryptoAlias taken to avoid ambiguity
from stocks.models import Securitie, Crypto as CryptoAlias
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site


class StockFilter(View):

    def get(self, request):
        exchange_to_search = []
        exchange_to_search.append('AMEX') if request.GET.get('AMEX', False) == 'on' else False
        exchange_to_search.append('NASDAQ') if request.GET.get('NASDAQ', False) == 'on' else False
        exchange_to_search.append('LSE') if request.GET.get('LSE', False) == 'on' else False
        exchange_to_search.append('NYSE') if request.GET.get('NYSE', False) == 'on' else False
        exchange_to_search.append('SGX') if request.GET.get('SGX', False) == 'on' else False

        if len(exchange_to_search) == 0:
            securities = Securitie.objects.all().order_by('?').last()
        else:
            securities = Securitie.objects.filter(exchange__in=exchange_to_search).order_by('?').last()

        context = {'symbol': securities.symbol,
                   'company_name': securities.name,
                   'listed_on': securities.exchange,
                   }

        return JsonResponse(context, status=200)


class PennyStocks(View):

    def get(self, request):
        securities_obj = Securitie.objects.filter(exchange__icontains='OTCBB').all().order_by('?').last()
        context = {'symbol': securities_obj.symbol,
                   'company_name': securities_obj.name,
                   'listed_on': securities_obj.exchange}

        return JsonResponse(context, status=201)


class Crypto(View):

    def get(self, request):
        crypto_obj = CryptoAlias.objects.filter().all().order_by('?').last()

        context = {'symbol': crypto_obj.symbol,
                   'company_name': crypto_obj.name,
                   'lookup': 'Coinbase'}

        return JsonResponse(context, status=200)


class Analysis(View):

    def get(self, request):
        symbol = request.GET.get('symbol')

        try:
            quote_table = si.get_quote_table(symbol)
        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Sorry! We don't have any data for that symbol"}, status=200)

        # field_names = ['symbol', 'oneYearTargetEst', 'fiftyTwoWeekRange',
        #           'ask', 'averageVolume', 'beta', 'bid', 'daysRange',
        #           'EPS', 'earningsDate', 'exDividendDate',
        #           'forwardDividendAndYield', 'marketCap', 'open',
        #           'peRatio', 'previousClose', 'quotePrice', 'volume']

        fields = ['1y Target Est', '52 Week Range', 'Ask', 'Avg. Volume',
                  'Beta (5Y Monthly)', 'Bid', "Day's Range", 'EPS (TTM)',
                  'Earnings Date', 'Ex-Dividend Date', 'Forward Dividend & Yield',
                  'Market Cap', 'Open', 'PE Ratio (TTM)', 'Previous Close',
                  'Quote Price', 'Volume']

        for key in fields:
            if type(quote_table[key]) != str:
                if isnan(quote_table[key]):
                    quote_table[key] = 'N/A'

        # {'1y Target Est': 9.0,
        #  '52 Week Range': '2.21 - 12.69',
        #  'Ask': '12.84 x 800',
        #  'Avg. Volume': 973371.0,
        #  'Beta (5Y Monthly)': 2.69,
        #  'Bid': '9.50 x 800',
        #  "Day's Range": '10.64 - 11.46',
        #  'EPS (TTM)': -24.64,
        #  'Earnings Date': 'Feb 18, 2021 - Feb 22, 2021',
        #  'Ex-Dividend Date': 'Mar 04, 2019',
        #  'Forward Dividend & Yield': 'N/A (N/A)',
        #  'Market Cap': '912.037M',
        #  'Open': 10.7,
        #  'PE Ratio (TTM)': nan,
        #  'Previous Close': 10.52,
        #  'Quote Price': 11.199999809265137,
        #  'Volume': 1063695.0}

        return JsonResponse(quote_table, status=200)


class BlogComment(View):

    def get(self, request):
        try:
            blog_id = request.GET.get('id')
            comments = Comment.objects.filter(object_pk=blog_id, is_public=True, is_removed=False,
                                              site=get_current_site(request), ).values_list('user__first_name',
                                                                                            'user__last_name',
                                                                                            'comment',
                                                                                            'submit_date'
                                                                                            ).order_by('-submit_date')
            # storing objects in an array to avoid serialization exception, serialization wil be done later on
            comments_arr = []
            for comment in comments:
                comments_arr.append(comment)
            return JsonResponse({'data': comments_arr}, status=200, safe=False)
        except Exception as e:
            return JsonResponse("Exception Occrred:" + str(e), status=400, safe=False)

    def post(self, request):

        if request.POST.get("comment") == '':
            return JsonResponse('Oops! No Comment found. Please add a comment', status=400, safe=False)

        if not request.user.is_authenticated:
            return JsonResponse("Please login first to add a comment", status=400, safe=False)

        content_type = ContentType.objects.get_for_model(Entry)
        object_id = request.POST.get("blogID")
        site = get_current_site(request)
        comment = request.POST.get("comment")
        ip_address = socket.gethostbyname(socket.gethostname())

        try:
            comment_obj = Comment(content_type=content_type, object_pk=object_id, site=site, user=request.user,
                                  comment=comment,
                                  ip_address=ip_address, is_public=True)
            comment_obj.save()
            return JsonResponse("Comment has been successfully added", status=200, safe=False)
        except Exception as e:
            return JsonResponse("Exception Occrred:" + str(e), status=400, safe=False)
