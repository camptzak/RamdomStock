from django.shortcuts import render
from django.views.generic import TemplateView
from stocks.models import Quote, Securitie, Crypto


class Home(TemplateView):
    template_name = 'stocks/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        securities_obj = Securitie.objects.all().order_by('?').last()
        quote_obj = Quote.objects.all().order_by('?').last()

        symbol = ''
        name = ''
        exchange = ''
        quote = ''
        author = ''

        if securities_obj is not None:
            symbol = securities_obj.symbol
            name = securities_obj.name
            exchange = securities_obj.exchange

        if quote_obj is not None:
            quote = quote_obj.quote
            author = quote_obj.author

        context = {'data': {'symbol': symbol,
                            'company_name': name,
                            'listed_on': exchange,
                            'quote': quote,
                            'quote_author': author
                            }}
        return context


class PennyStocks(TemplateView):
    template_name = 'stocks/penny_stocks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        quote_obj = Quote.objects.all().order_by('?').last()
        securities_obj = Securitie.objects.filter(exchange__icontains='OTCBB').all().order_by('?').last()
        context = {'data': {'symbol': securities_obj.symbol,
                            'company_name': securities_obj.name,
                            'listed_on': securities_obj.exchange,
                            'quote': quote_obj.quote,
                            'quote_author': quote_obj.author
                            }}
        return context


class CryptoStocks(TemplateView):
    template_name = 'stocks/crypto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        quote_obj = Quote.objects.all().order_by('?').last()
        crypto_obj = Crypto.objects.all().order_by('?').last()
        context = {'data': {'symbol': crypto_obj.symbol,
                            'company_name': crypto_obj.name,
                            'lookup': 'Coinbase',
                            'quote': quote_obj.quote,
                            'quote_author': quote_obj.author
                            }}
        return context


class Analysis(TemplateView):
    template_name = 'stocks/analysis.html'

    def post(self, request):
        return render(request, self.template_name, {'symbol': request.POST.get('symbol')})

