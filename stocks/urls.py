from django.conf.urls import url
from django.urls import path, include
from stocks.views import Home, CustomUserCreationForm, PennyStocks, CryptoStocks
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Home.as_view()),
    path('penny-stocks/', PennyStocks.as_view()),
    path('crypto/', CryptoStocks.as_view()),
    path('register/', CustomUserCreationForm.as_view(), name='Register'),

    # url(r'^weblog/', include('zinnia.urls')),
    # url(r'^comments/', include('django.contrib.comments.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
