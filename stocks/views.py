from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django import forms
from django.contrib import messages
import hashlib
import os
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView
from httplib2 import Response
from randomstock.settings import STATIC_URL, STATIC_ROOT
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet

from stocks.models import Securitie, User, Quote, Crypto
from stocks.serializers import SecuritiesSerializer


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

        return JsonResponse(context, status=201)


class CustomUserCreationForm(forms.Form, View):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    template_name = 'register.html'

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):

        password = self.cleaned_data['password1']
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password_hash=hashed_password
        )
        return user

    def post(self, request):

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('error.html')
        else:
            return redirect('error.html')

        return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})


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
        crypto_obj = Crypto.objects.filter(exchange__icontains='OTCBB').all().order_by('?').last()
        context = {'data': {'symbol': crypto_obj.symbol,
                            'company_name': crypto_obj.name,
                            'quote': quote_obj.quote,
                            'quote_author': quote_obj.author
                            }}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        crypto_obj = Crypto.objects.filter().all().order_by('?').last()
        context = {'symbol': crypto_obj.symbol,
                   'company_name': crypto_obj.name}
        return JsonResponse(context, status=201)
