from django.contrib import admin
from custom_all_auth.models import UserProfile
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp


# TODO: Code of combining the user and profile model in 1 screen: needs to be corrected a bit then uncomment the code
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
#     # fields = ('username', ('first_name', 'last_name'), 'email', 'is_staff', 'is_active', 'is_superuser',
#     #           'last_login', 'date_joined')
#
#     inlines = [
#         UserProfileInline
#     ]
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


# IMPORTANT
admin.autodiscover()

admin.site.register(UserProfile)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
