from django.urls import path

from bookshelf.views import home_view, book_view, pdf_reader, ajax_pdf_response, loan_request_view, \
    request_history_view, remove_request_ajax, book_audio

app_name = 'bookshelf'

urlpatterns = [
    path('', home_view, name='home'),
    # path('categories/', categories_view, name='categories'),
    path('id=<int:book_id>&name=<str:book_name>/', book_view, name='book_details'),
    path('pdf-reader/id=<int:book_id>&<str:t>/', pdf_reader, name='pdf_reader'),
    path('pdf-data/', ajax_pdf_response, name='pdf_data'),
    path('loan-request/book-id=<int:book_id>/', loan_request_view, name='loan_request'),
    path('request-history/', request_history_view, name='request_history'),
    path('remove_request/', remove_request_ajax, name='remove_request'),
    path('book-audio/id=<int:book_id>&name=<str:book_name>/', book_audio, name='book-audio'),
]