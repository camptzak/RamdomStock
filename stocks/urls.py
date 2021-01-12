from django.conf.urls import url
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from stocks.views import Home, Register, PennyStocks, CryptoStocks, BlogView, BlogDetailsView, \
    BlogViewSet, AnalysisView, Login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Home.as_view()),
    path('penny-stocks/', PennyStocks.as_view()),
    path('crypto/', CryptoStocks.as_view()),
    path('register/', Register.as_view(), name='Register'),
    path('login/', Login.as_view()),
    path('blog/', BlogView.as_view(), name='Blog'),
    path('post-blog/', csrf_exempt(BlogDetailsView.as_view()), name='PostBlog'),
    path('list-blogs/', csrf_exempt(BlogViewSet.as_view()), name='BlogDetails'),
    path('analysis/', csrf_exempt(AnalysisView.as_view()), name='Analysis')

    # url(r'^weblog/', include('zinnia.urls')),
    # url(r'^comments/', include('django.contrib.comments.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
