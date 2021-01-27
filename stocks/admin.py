from django.contrib import admin
from zinnia.models import Category
from tagging.models import Tag, TaggedItem
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from RandomStock.settings import ADMIN_ORDERING
from .models import Securitie, Crypto, Quote, PennyStock


class SecuritieAdmin(admin.ModelAdmin):
    model = Securitie
    list_display = ['symbol', 'name', 'exchange']
    search_fields = ['symbol', 'name', 'exchange']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(exchange__icontains='OTCBB').all()


class PennyStocksAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'exchange']
    search_fields = ['symbol', 'name', 'exchange']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(exchange__icontains='OTCBB').all()


class CryptoAdmin(admin.ModelAdmin):
    model = Crypto
    list_display = ['symbol', 'name', 'lookup']
    search_fields = ['symbol', 'name', 'lookup']


class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ['author', 'quote']
    search_fields = ['author', 'quote']


# function for reording of models in admin site
def get_app_list(self, request):
    try:
        app_dict = self._build_app_dict(request)
        for app_name, object_list in ADMIN_ORDERING:
            ('zinnia', [
                'Entry',
            ]),
            app = app_dict[app_name]
            app['models'].sort(key=lambda x: object_list.index(x['object_name']))
            yield app
    except:
        app = app_dict['zinnia']
        yield app


# Covering django.contrib.admin.AdminSite.get_app_list
admin.AdminSite.get_app_list = get_app_list

# IMPORTANT
admin.autodiscover()

admin.site.register(Securitie, SecuritieAdmin)
admin.site.register(PennyStock, PennyStocksAdmin)
admin.site.register(Crypto, CryptoAdmin)
admin.site.register(Quote, QuoteAdmin)

admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.unregister(Tag)
admin.site.unregister(TaggedItem)

admin.site.unregister(Category)
