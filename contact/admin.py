from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from contact.models import RequestLoan, AvailableDate


@admin.register(RequestLoan)
class RequestLoanAdmin(admin.ModelAdmin):
    list_display = (
        ('date_of_placed_request', JDateFieldListFilter)[0],
        'user',
        'book',
        ('date_of_request', JDateFieldListFilter)[0],
        'hour',
        'description',
        'is_request_processed',
    )
    list_filter = (
        'is_request_processed',
    )
    readonly_fields = (
        'date_of_placed_request',
    )
    search_fields = ('user__username',)
    fields = (
        ('date_of_placed_request', JDateFieldListFilter)[0],
        'user',
        'book',
        ('date_of_request', JDateFieldListFilter)[0],
        'hour',
        'description',
        'is_request_processed',
    )


@admin.register(AvailableDate)
class AvailableDateAdmin(admin.ModelAdmin):
    list_display = (
        ('available_date', JDateFieldListFilter)[0],
        'from_hour',
        'to_hour',
    )
    fields = (
        ('available_date', JDateFieldListFilter)[0],
        'from_hour',
        'to_hour',
    )
