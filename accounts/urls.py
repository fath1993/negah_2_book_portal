from django.urls import path
from accounts.views import signup_view, login_view, logout_view, \
    ajax_add_message_to_read_group, \
    profile_view, personal_library, loan_request_view, request_history_view, remove_request_ajax, \
    ajax_remove_book_from_reading_state, ajax_user_message_state, user_report_view
from bookshelf.views import ajax_add_book_to_wish_list, ajax_remove_book_from_wish_list, ajax_add_book_to_liked_list, \
    ajax_remove_book_from_liked_list

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),

    path('personal-library/', personal_library, name='personal-library'),
    path('loan-request/book-id=<int:book_id>/', loan_request_view, name='loan-request'),
    path('request-history/', request_history_view, name='request-history'),
    path('remove_request/', remove_request_ajax, name='remove-request'),
    path('user-report-view/', user_report_view, name='user-report-view'),


    path('ajax-add-book-to-wish-list/', ajax_add_book_to_wish_list, name='ajax-add-book-to-wish-list'),
    path('ajax-remove-book-from-wish-list/', ajax_remove_book_from_wish_list, name='ajax-remove-book-from-wish-list'),
    path('ajax-add-book-to-liked-list/', ajax_add_book_to_liked_list, name='ajax-add-book-to-liked-list'),
    path('ajax-remove-book-from-liked-list/', ajax_remove_book_from_liked_list, name='ajax-remove-book-from-liked-list'),



    path('ajax-remove-book-from-reading-state/', ajax_remove_book_from_reading_state, name='ajax-remove-book-from-reading-state'),
    path('ajax_add_message_to_read_group/', ajax_add_message_to_read_group, name='ajax_add_message_to_read_group'),
    path('ajax-user-message-state/', ajax_user_message_state, name='ajax-user-message-state'),
]