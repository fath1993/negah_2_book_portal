from django.urls import path
from accounts.views import signup_view, login_view, logout_view, personal_library, ajax_add_book_to_profile, \
    ajax_remove_book_from_profile, ajax_add_notification_to_read_group, ajax_add_message_to_read_group

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('personal-library/', personal_library, name='personal-library'),
    path('ajax_add_book_to_profile/', ajax_add_book_to_profile, name='ajax_add_book_to_profile'),
    path('remove-book-from-profile/', ajax_remove_book_from_profile, name='remove-book-from-profile'),
    path('ajax_add_notification_to_read_group/', ajax_add_notification_to_read_group, name='ajax_add_notification_to_read_group'),
    path('ajax_add_message_to_read_group/', ajax_add_message_to_read_group, name='ajax_add_message_to_read_group'),
]