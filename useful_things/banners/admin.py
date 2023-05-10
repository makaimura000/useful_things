from django.contrib import admin
from .models import Banner
from django.utils.html import format_html

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'banner', 'is_active')
    list_editable = ('is_active',)

    def image_tag(self, obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))
