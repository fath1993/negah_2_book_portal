from django.contrib import admin

from file_gallery.models import FileGallery


@admin.register(FileGallery)
class FileGalleryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file_alt',
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )

    fields = (
        'file_alt',
        'file_src',
        'created_at',
    )
