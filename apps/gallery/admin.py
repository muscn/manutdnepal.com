from django.contrib import admin
from .models import Album, Image


class ImageInline(admin.TabularInline):
    model = Image


class AlbumAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Album, AlbumAdmin)
admin.site.register(Image)
# Register your models here.
