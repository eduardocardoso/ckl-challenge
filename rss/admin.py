import datetime

from django.contrib import admin
from django.utils import timezone
from django import forms

from .feed import RSSFeed
from .models import Outlet
# Register your models here.

class OutletAdminForm(forms.ModelForm):
    class Meta:
        model = Outlet
        fields = ['rss_url', 'name', 'description', 'url', 'language', 'updated']
        readonly_fields = ['name', 'url', 'description', 'language', 'updated']

    def clean(self):
        """
        Fetch information about the outlet before saving
        :return:
        """
        rss_url = self.cleaned_data.get('rss_url')
        try:
            feed = RSSFeed(rss_url)
            channel_info = feed.get_channel_info()
        except ValueError, e:
            raise forms.ValidationError(e.message)

        self.instance.name = channel_info['title']
        self.instance.description = channel_info['subtitle']
        self.instance.url = channel_info['url']
        self.instance.language = channel_info['language']
        self.instance.updated = None

        return self.cleaned_data


class OutletAdmin(admin.ModelAdmin):
    form = OutletAdminForm
    fieldsets = [
        (None, {'fields': ['rss_url']}),
        ('Channel Information', {
            'fields': ['name', 'description', 'url', 'language', 'updated']
        }),
    ]
    readonly_fields = ['name', 'url', 'description', 'language', 'updated']
    list_display = ['name', 'url', 'rss_url', 'updated']
    ordering = ['name']


admin.site.register(Outlet, OutletAdmin)