from django.views.decorators.csrf import csrf_exempt

from . import views
from django.urls import path

# NOTE: URLs naming convention is kept in Pascal on purpose due to business requirement
urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('PennyStocks/', views.PennyStocks.as_view(), name='penny_stocks'),
    path('crypto/', views.CryptoStocks.as_view(), name='crypto'),
    path('analysis/', csrf_exempt(views.Analysis.as_view()), name='analysis'),
]
