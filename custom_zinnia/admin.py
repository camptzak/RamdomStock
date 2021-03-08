from django.contrib import admin
from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin
from zinnia_ckeditor.admin import EntryAdminCKEditor

# IMPORTANT
admin.autodiscover()


def _(param):
    pass


class EntryAdminCKEditorAdmin(EntryAdminCKEditor, EntryAdmin):
    EntryAdmin.list_display = ['title', 'is_visible', 'publication_date', 'slug']
    EntryAdmin.view_on_site = False

    # EntryAdmin.fields = (('title', 'status'), 'lead', 'content', 'image', 'publication_date', 'slug')
    # EntryAdmin.fieldsets = (
    #     ['Main', {
    #         'fields': (('title', 'status'), 'lead', 'content',  'slug')
    #     }],
    #     ['Advance', {
    #         'classes': ('collapse',),  # CSS
    #         'fields': ('illustration',),
    #     }]
    # )


admin.site.unregister(Entry)
admin.site.register(Entry, EntryAdminCKEditor)
