from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django import forms

from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView
from httplib2 import Response
from randomstock.settings import STATIC_URL, STATIC_ROOT
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet

from stocks.models import Securities, Users
from stocks.serializers import SecuritiesSerializer


class Home(View):

    template_name = 'home.html'

    def get(self, request):
        securities = Securities.objects.all().order_by('?').last()

        context = {'data': {'symbol': securities.symbol,
                            'company_name': securities.name,
                            'listed_on': securities.exchange}}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):

        exchange_to_search = []
        exchange_to_search.append('AMEX') if request.POST.get('amex', False) != 'false' else False
        exchange_to_search.append('NASDAQ') if request.POST.get('nasdaq', False) != 'false' else False
        exchange_to_search.append('LSE') if request.POST.get('lse', False) != 'false' else False
        exchange_to_search.append('NYSE') if request.POST.get('nyse', False) != 'false' else False
        exchange_to_search.append('SGX') if request.POST.get('sgx', False) != 'false' else False

        if len(exchange_to_search) == 0:
            securities = Securities.objects.all().order_by('?').last()
        else:
            securities = Securities.objects.filter(exchange__in=exchange_to_search).order_by('?').last()

        context = {'symbol': securities.symbol,
                   'company_name': securities.name,
                   'listed_on': securities.exchange}

        return JsonResponse(context, status=201)


class CustomUserCreationForm(forms.Form, View):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Users.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Users.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = Users.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class Register(View, UserCreationForm):

    template_name = 'register.html'
    def post(self, response):
        # passwords do not match
        if response.POST['password1'] != response.POST['password2']:
            form = CustomUserCreationForm(response.POST)
            return render(response, 'signup.html', {'form': form, 'pass_dont_match': True})

        if self.add_user(response.POST):
            # username + password are OK
            return redirect(reverse('Upload', kwargs={'username': response.POST['username']}))
        else:
            # username already exists
            form = CustomUserCreationForm(response.POST)
            return render(response, 'register.html', {'form': form, 'exists': True})

    def get(self, request):
        form = CustomUserCreationForm(request.POST)
        return render(request, 'register.html', {'form': form})

    def add_user(self, data):
        try:
            Users.objects.get(username=data['username'])    # user already exists
            return False
        except Users.DoesNotExist:  # user does not exist in DB table users
            print('create a new user')
            Users.objects.create(username=data['username'], password=data['password1'])
        return True
