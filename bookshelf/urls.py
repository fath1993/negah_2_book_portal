from django.urls import path

from bookshelf.views import home_view, book_view, pdf_reader, ajax_pdf_response, book_audio, filter_view

app_name = 'bookshelf'

urlpatterns = [
    path('', home_view, name='home'),
    path('filters/', filter_view, name='filters'),
    path('id=<int:book_id>&name=<str:book_name>/', book_view, name='book_details'),
    path('pdf-reader/id=<int:book_id>&<str:t>/', pdf_reader, name='pdf_reader'),
    path('pdf-data/', ajax_pdf_response, name='pdf_data'),

    path('book-audio/id=<int:book_id>&name=<str:book_name>/', book_audio, name='book-audio'),
]