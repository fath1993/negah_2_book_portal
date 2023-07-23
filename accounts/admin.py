from django.contrib import admin
from accounts.models import UserProfile, Message, UserBookAssign, UserBookStatus


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'is_message_seen',
    )

    search_fields = (
        'user',
    )

    fields = (
        'user',
        'profile_image',
        'is_message_seen',
        'specific_book_only_for_this_user',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'content',
        'created_at_display',
    )

    readonly_fields = (
        'created_at',
    )

    fields = (
        'users',
        'content',
        'created_at',
    )

    @admin.display(description="تاریخ ایجاد", empty_value='???')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')


@admin.register(UserBookStatus)
class UserBookStatusAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'book',
        'is_reading',
        'reading_started_at',
        # 'is_finished',
        # 'is_Wished',
        # 'is_liked',
    )

    readonly_fields = (
        'user',
        'book',
        'is_reading',
        'reading_started_at',
        # 'last_page',
        # 'is_finished',
        # 'finish_time',
        # 'is_Wished',
        # 'wish_time',
        # 'is_liked',
        # 'like_time',
    )

    fields = (
        'user',
        'book',
        'is_reading',
        'reading_started_at',
        # 'last_page',
        # 'is_finished',
        # 'finish_time',
        # 'is_Wished',
        # 'wish_time',
        # 'is_liked',
        # 'like_time',
    )


@admin.register(UserBookAssign)
class UserBookAssignAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'book',
        'date_of_assignment_display',
        'date_of_return_display',

    )

    readonly_fields = (
        'date_of_assignment',
    )

    fields = (
        'user',
        'book',
        'date_of_assignment',
        'date_of_return',

    )

    @admin.display(description="تاریخ امانت گرفتن", empty_value='???')
    def date_of_assignment_display(self, obj):
        return obj.date_of_assignment.strftime('%Y-%m-%d %H:%M')

    @admin.display(description="تاریخ بازگردانی", empty_value='???')
    def date_of_return_display(self, obj):
        return obj.date_of_return.strftime('%Y-%m-%d %H:%M')
