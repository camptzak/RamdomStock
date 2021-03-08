from django.urls import path, include
from allauth.account.views import SignupView


urlpatterns = [
    path('', include('allauth.urls')),
    path('register/', SignupView.as_view(), name="account_signup"),
]
