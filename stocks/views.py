import json
import hashlib
import yahoo_fin.stock_info as si

from math import isnan
from django import forms
from django.views import View
from zinnia.models import Entry
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from stocks.serializers import SecuritiesSerializer, EntrySerializer
from stocks.models import Securitie, Profile, Quote, Crypto, BlogInfo


# helper function
def hash_password(pass1):
    return hashlib.sha256(pass1.encode("utf-8")).hexdigest()


class Register(forms.Form, View):
    username = forms.CharField(min_length=4, max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    template_name = 'register.html'

    def post(self, request):

        data = request.POST
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if email is not None:
            email = email.lower()
            r = User.objects.filter(email=email)
            if r.count():
                raise ValidationError("Email already exists")
        else:
            raise ValidationError("Email not provided")

        if username is not None:
            username = username.lower()
            r = User.objects.filter(username=username)
            if r.count():
                raise ValidationError("Username already exists")
        else:
            raise ValidationError("Username not provided")

        if password is not None:
            # creating new user
            password_hashed = hash_password(password)
            user = User.objects.create_user(username=username, email=email)
            user.password = password_hashed
            user.save()
            profile = Profile.objects.create(user=user)

        return render(request, 'login.html', {'logged in': True})

    def get(self, request):
        form = Register()
        return render(request, self.template_name, {'form': form})


class Login(View):
    template = 'login.html'

    def get(self, request):
        return render(request, self.template, {})

    def post(self, response):
        username = response.POST.get('username', None)
        password = response.POST.get('password', None)
        if (username is None) or (password is None):
            raise ValidationError("missing details")

        password_hashed = hash_password(password)

        try:
            user_obj = User.objects.get(username=username, password=password_hashed)
        except User.DoesNotExist:  # if username does not exists
            return render(response, self.template, {'not_exists': True})

        token, created = Token.objects.get_or_create(user=user_obj)
        return render(response, 'home.html', {'token': token.key})


class Home(View):

    template_name = 'home.html'

    def get(self, request):
        securities_obj = Securitie.objects.all().order_by('?').last()
        quote_obj = Quote.objects.all().order_by('?').last()

        context = {'data': {'symbol': securities_obj.symbol,
                            'company_name': securities_obj.name,
                            'listed_on': securities_obj.exchange,
                            'quote': quote_obj.quote,
                            'quote_author': quote_obj.author
                            }}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):

        exchange_to_search = []
        exchange_to_search.append('AMEX') if request.POST.get('amex', False) != 'false' else False
        exchange_to_search.append('NASDAQ') if request.POST.get('nasdaq', False) != 'false' else False
        exchange_to_search.append('LSE') if request.POST.get('lse', False) != 'false' else False
        exchange_to_search.append('NYSE') if request.POST.get('nyse', False) != 'false' else False
        exchange_to_search.append('SGX') if request.POST.get('sgx', False) != 'false' else False

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
    template_name = 'penny_stocks.html'

    def get(self, request):
        quote_obj = Quote.objects.all().order_by('?').last()
        securities_obj = Securitie.objects.filter(exchange__icontains='OTCBB').all().order_by('?').last()
        context = {'data': {'symbol': securities_obj.symbol,
                            'company_name': securities_obj.name,
                            'listed_on': securities_obj.exchange,
                            'quote': quote_obj.quote,
                            'quote_author': quote_obj.author
                            }}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        securities_obj = Securitie.objects.filter(exchange__icontains='OTCBB').all().order_by('?').last()
        context = {'symbol': securities_obj.symbol,
                   'company_name': securities_obj.name,
                   'listed_on': securities_obj.exchange}
        return JsonResponse(context, status=201)


class CryptoStocks(View):
    template_name = 'crypto.html'

    def get(self, request):
        quote_obj = Quote.objects.all().order_by('?').last()
        crypto_obj = Crypto.objects.all().order_by('?').last()
        context = {'data': {'symbol': crypto_obj.symbol,
                            'company_name': crypto_obj.name,
                            'lookup': 'Coinbase',
                            'quote': quote_obj.quote,
                            'quote_author': quote_obj.author
                            }}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        crypto_obj = Crypto.objects.filter().all().order_by('?').last()
        context = {'symbol': crypto_obj.symbol,
                   'company_name': crypto_obj.name,
                   'lookup': 'Coinbase'}
        return JsonResponse(context, status=200)


class BlogView(View):
    template = 'blog_details.html'

    def get(self, request):
        return render(request, template_name=self.template_name, context={})


class BlogViewSet(ListAPIView):
    serializer_class = EntrySerializer
    pagination_class = PageNumberPagination

    # get the list of all blogs
    def get(self, request, *args, **kwargs):
        self.queryset = Entry.objects.all()
        return self.list(request, *args, **kwargs)


class BlogDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    template = 'blog_details.html'

    def get(self, request):
        pass
        # return render(request, template_name=self.template_name, context={})

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            raise ValidationError('Error reading body of request')

        # change this to authenticate from django user
        user_id = request.user
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            ValidationError('user does not exist')

        text = data.get('text', None)
        brief_description = data.get('brief_description', None)
        title = data.get('title', None)
        publication_date = data.get('publication_date', None)

        if (text is None) or (brief_description is None) or (title is None):
            return JsonResponse({'Error': 'missing fields'}, status=201)

        try:
            if publication_date is None:
                blog = Entry.objects.create(brief_description=text,
                                            user=user,
                                            title=title,
                                            text=brief_description
                                            )
            else:
                blog = Entry.objects.create(brief_description=text,
                                            user=user,
                                            title=title,
                                            text=brief_description,
                                            # publication_date=publication_date
                                            )
        except Exception as e:
            return render(request, template_name=self.template_name, context={'Error': 'Something went wrong'})

        return JsonResponse({'Success': 'Blog created'}, status=201)


class AnalysisView(View):
    template = 'analysis.html'

    def get(self, request):
        return render(request, template_name=self.template_name, context={})

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        symbol = data.get('symbol', None)

        try:
            quote_table = si.get_quote_table(symbol)
        except Exception as e:
            return JsonResponse({"Error": "Sorry! We don't have any data for that symbol"}, status=200)

        # field_names = ['symbol', 'oneYearTargetEst', 'fiftyTwoWeekRange',
        #           'ask', 'averageVolume', 'beta', 'bid', 'daysRange',
        #           'EPS', 'earningsDate', 'exDividendDate',
        #           'forwardDividendAndYield', 'marketCap', 'open',
        #           'peRatio', 'previousClose', 'quotePrice', 'volume']

        fields = ['1y Target Est', '52 Week Range', 'Ask', 'Avg. Volume',
                  'Beta (5Y Monthly)', 'Bid', "Day's Range", 'EPS (TTM)',
                  'Earnings Date',  'Ex-Dividend Date', 'Forward Dividend & Yield',
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
