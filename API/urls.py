from API import views
from django.urls import path


# NOTE: URLs naming convention is kept in Pascal on purpose due to business requirement
urlpatterns = [
    path('FilterStocks', views.StockFilter.as_view(), name='filterStocksAPI'),
    path('PennyStocks', views.PennyStocks.as_view(), name='pennyStocksAPI'),
    path('Crypto', views.Crypto.as_view(), name='cryptoAPI'),
    path('Analysis', views.Analysis.as_view(), name='analysisAPI'),
    path('Comment', views.BlogComment.as_view(), name='blogComment'),

]
