from django.contrib import admin
from zinnia.models import Category
from tagging.models import Tag, TaggedItem
from .models import Securitie, Crypto, Quote
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site


class SecuritieAdmin(admin.ModelAdmin):
    model = Securitie
    list_display = ['symbol', 'name', 'exchange']
    search_fields = ['symbol', 'name', 'exchange']


class CryptoAdmin(admin.ModelAdmin):
    model = Crypto
    list_display = ['symbol', 'name', 'lookup']
    search_fields = ['symbol', 'name', 'lookup']


class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ['author', 'quote']
    search_fields = ['author', 'quote']


# IMPORTANT
admin.autodiscover()

admin.site.register(Securitie, SecuritieAdmin)
admin.site.register(Crypto, CryptoAdmin)
admin.site.register(Quote, QuoteAdmin)

admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.unregister(Tag)
admin.site.unregister(TaggedItem)

admin.site.unregister(Category)


