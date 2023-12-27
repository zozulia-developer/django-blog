from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from . import models


class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'image', 'image_img', 'date_pub')
    readonly_fields = ('image_img',)
    list_filter = ('status',)
    search_fields = ('title', 'status',)
    summernote_fields = ('body',)


admin.site.register(models.Post, ArticleAdmin)
admin.site.register(models.Tag)
