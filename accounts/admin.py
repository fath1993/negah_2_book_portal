from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from accounts.models import UserProfile, Notification, PrivateMessage, Message, UserBookAssign, UserBookStatus


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

    search_fields = (
        'user',
    )

    fields = (
        'user',
        'profile_image',
        'reading_book',
        'wish_list',
        'notification_box',
        'is_notification_seen',
        'message_box',
        'is_message_seen',
        'specific_book_only_for_this_user',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'message',
        ('time', JDateFieldListFilter)[0],
    )
    readonly_fields = (
        'time',
    )
    fields = (
        'message',
        ('time', JDateFieldListFilter)[0],
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'receivers_name',
        'notification',
    )

    fields = (
        'notification',
    )

    @admin.display(description="کاربران دریافت کننده", empty_value='???')
    def receivers_name(self, obj):
        return 'همه'


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = (
        'receivers_name',
        'private_message',
    )

    fields = (
        'users',
        'private_message',
    )

    @admin.display(description="کاربران دریافت کننده", empty_value='???')
    def receivers_name(self, obj):
        list_names = ''
        for user in obj.users.all():
            list_names = list_names + ", " + str(user.username)
        return list_names



@admin.register(UserBookStatus)
class UserBookStatusAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'book',
        'is_reading',
        'is_finished',
        'is_Wished',
        'is_liked',
    )

    readonly_fields = (
        'user',
        'book',
        'is_reading',
        'last_page',
        'is_finished',
        'finish_time',
        'is_Wished',
        'wish_time',
        'is_liked',
        'like_time',
    )

    fields = (
        'user',
        'book',
        'is_reading',
        'last_page',
        'is_finished',
        'finish_time',
        'is_Wished',
        'wish_time',
        'is_liked',
        'like_time',
    )


@admin.register(UserBookAssign)
class UserBookAssignAdmin(admin.ModelAdmin):
    list_display = (
        'book_borrower',
        'book_title',
        ('date_of_assignment', JDateFieldListFilter)[0],
        ('date_of_return', JDateFieldListFilter)[0],
        'is_this_book_returned',

    )

    search_fields = (
        'date_of_assignment',
        'borrower__username',
        'book__title',

    )
    list_filter = (
        'date_of_assignment',
        'is_this_book_returned',
    )
    readonly_fields = (
        'is_this_book_returned',
        'date_of_assignment',
    )

    fields = (
        'book',
        'borrower',
        ('date_of_assignment', JDateFieldListFilter)[0],
        ('date_of_return', JDateFieldListFilter)[0],
        'is_this_book_returned',

    )

    @admin.display(description="نام کتاب", empty_value='???')
    def book_title(self, obj):
        return obj.book.title

    @admin.display(description="نام قرض گیرنده", empty_value='???')
    def book_borrower(self, obj):
        return obj.borrower.username
