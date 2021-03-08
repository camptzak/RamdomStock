from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('stocks.urls')),
                  path('', include('custom_all_auth.urls')),
                  path('API/', include('API.urls')),
                  path('', include('custom_zinnia.urls')),
                  re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = 'Random Stock Administration'
admin.site.site_header = 'Random Stock Admin'
admin.site.index_title = 'Random Stock Administration'
