from django.contrib import admin
from bookshelf.models import BookInvolvedPerson, MagicWord, Publisher, Book, BookProfile


@admin.register(BookInvolvedPerson)
class BookInvolvedPersonAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'role',
    )

    list_filter = (
        'role',
    )

    fields = (
        'full_name',
        'images',
        'role',
    )


@admin.register(MagicWord)
class MagicWordAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'word_type',
    )

    list_filter = (
        'word_type',
    )

    readonly_fields = (
        'slug_title',
    )

    fields = (
        'title',
        'slug_title',
        'word_type',
    )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = (
        'publisher_name',
        'publisher_address',
    )

    fields = (
        'publisher_name',
        'publisher_address',
    )



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'book_summery',
    )

    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )
    fields = (
        'id',
        'title',
        'authors',
        'interpreters',
        'publisher',
        'publish_place',
        'publish_year',
        'date_of_publish',
        'language',
        'ISBN',
        'subjects',
        'categories',
        'keywords',
        'classification',
        'registration_number',
        'version',
        'on_paper_image',
        'book_images',
        'summery',
        'number_of_pages',
        'created_at',
        'updated_at',
    )

    @admin.display(description="خلاصه", empty_value='???')
    def book_summery(self, obj):
        return obj.summery[:100] + "..."


@admin.register(BookProfile)
class BookProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'book',
        'number_of_inventory',
        'is_published_on_site',
    )

    readonly_fields = (
        'id',
        'book',
    )

    fields = (
        'book',
        'pdf_demo',
        'pdf_source',
        'audio_demo',
        'audio_source',
        'audio_speaker',
        'review',
        'visited_by_users',
        'number_of_inventory',
        'is_published_on_site',
    )

    @admin.display(description="خلاصه", empty_value='???')
    def book_summery(self, obj):
        return obj.summery[:100] + "..."


