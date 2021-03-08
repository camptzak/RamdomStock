from django.contrib import admin
from custom_all_auth.models import UserProfile
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp, EmailAddress
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserAddForm(UserCreationForm):

    def full_clean(self):
        data = self.data.copy()

        if type(data.get('groups', None)) != 'list':
            data['groups'] = [self.data.get('groups')] if self.data.get('groups', False) else []
        self.data = data
        return super().full_clean()

    def _save_m2m(self):
        super()._save_m2m()

        instance = self.instance
        if instance.groups.filter(name='Admin').count() > 0:
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()

        elif instance.groups.filter(name='Writer').count() > 0:
            instance.is_staff = True
            instance.is_superuser = False
            instance.save()

        elif instance.groups.filter(name='Website_user').count() > 0:
            instance.is_staff = False
            instance.is_superuser = False
            instance.save()

    class Meta(UserCreationForm.Meta):
        widgets = {
            'groups': forms.Select()
        }
        # fields = ('username', 'groups')


class UserUpdateForm(UserChangeForm):

    def full_clean(self):
        data = self.data.copy()

        if type(data.get('groups', None)) != 'list':
            data['groups'] = [self.data.get('groups')] if self.data.get('groups', False) else []
        self.data = data
        return super().full_clean()

    def _save_m2m(self):
        super()._save_m2m()

        instance = self.instance
        if instance.groups.filter(name='Admin').count() > 0:
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()

        elif instance.groups.filter(name='Writer').count() > 0:
            instance.is_staff = True
            instance.is_superuser = False
            instance.save()

        elif instance.groups.filter(name='Website_user').count() > 0:
            instance.is_staff = False
            instance.is_superuser = False
            instance.save()

    class Meta(UserCreationForm.Meta):
        widgets = {
            'groups': forms.Select()
        }
        # fields = ('username', 'groups')


class ExtendedUserAdmin(UserAdmin):
    add_form = UserAddForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_active', 'groups')
        }),
    )
    form = UserUpdateForm
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'groups', 'date_joined')
        }),
    )

    inlines = [
        UserProfileInline
    ]


# IMPORTANT
admin.autodiscover()

# admin.site.register(UserProfile)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(EmailAddress)

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)

