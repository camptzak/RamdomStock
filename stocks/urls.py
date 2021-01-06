from django.conf.urls import url
from django.urls import path, include
from stocks.views import Home, RegisterForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Home.as_view()),
    path('register/', RegisterForm.as_view(), name='Register'),

    # url(r'^weblog/', include('zinnia.urls')),
    # url(r'^comments/', include('django.contrib.comments.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
