from django.contrib import admin
from website.models import HomePageSliderImage, BooOfTheWeek, FeaturedBook


@admin.register(HomePageSliderImage)
class HomePageSliderImageAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'image',
    )

    fields = (
        'order_id',
        'image',
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(BooOfTheWeek)
class BooOfTheWeekAdmin(admin.ModelAdmin):
    list_display = (
        'book',
    )

    fields = (
        'book',
    )

    raw_id_fields = (
        'book',
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(FeaturedBook)
class FeaturedBookAdmin(admin.ModelAdmin):
    list_display = (
        'book',
    )

    fields = (
        'book',
    )

    raw_id_fields = (
        'book',
    )