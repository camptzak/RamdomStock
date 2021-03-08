from django.urls import path, include
from . import views

urlpatterns = [
    path('blog/', views.Blog.as_view(), name='blog'),
    path('<slug:slug>/', views.BlogDetail.as_view(), name='blogDetails'),
    path('weblog/', include('zinnia.urls')),
]
