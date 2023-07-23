import threading

import jdatetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from accounts.models import UserProfile, UserBookAssign, UserBookStatus
from bookshelf.models import Book, BookProfile, MagicWord
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from contact.models import AvailableDate, RequestLoan
from website.models import HomePageSliderImage, BooOfTheWeek, FeaturedBook


def home_view(request):
    context = {'page_title': 'صفحه اصلی'}
    if request.user.is_authenticated:
        if request.method == 'GET':
            book_profiles = BookProfile.objects.filter(is_published_on_site=True)[:12]
            context['book_profiles'] = book_profiles
            featured_books = FeaturedBook.objects.filter()
            if featured_books.count() >= 8:
                context['featured_books'] = featured_books
            else:
                context['featured_books'] = []
            try:
                book_of_the_week = BooOfTheWeek.objects.filter().latest('id')
                context['book_of_the_week'] = book_of_the_week
            except:
                pass

            home_page_slider_images = HomePageSliderImage.objects.filter()
            context['home_page_slider_images'] = home_page_slider_images

            return render(request, 'index.html', context)
        else:
            return JsonResponse({'message': 'not allowed'})
    else:
        return redirect('accounts:login')


def filter_view(request):
    context = {'page_title': 'صفحه دسته بندی و فیلتر کتاب ها'}
    if request.user.is_authenticated:
        books = []
        if request.method == 'GET':
            book_profiles = BookProfile.objects.filter(is_published_on_site=True).order_by('id')
            for book in book_profiles:
                books.append(book.book)
            context['books'] = set(books)
            magic_words = MagicWord.objects.filter()
            context['categories'] = magic_words.filter(word_type='category')
            context['keywords'] = magic_words.filter(word_type='keyword')
            context['subject'] = magic_words.filter(word_type='subject')
            return render(request, 'book-filters.html', context)
        else:
            try:
                mark = str(request.POST['mark'])
                if mark == 'بر اساس':
                    mark = None
            except:
                mark = None
            try:
                category = str(request.POST['category'])
                if category == 'دسته':
                    category = None
            except:
                category = None
            try:
                year_of_publish = str(request.POST['year_of_publish'])
                if year_of_publish == 'سال انتشار':
                    year_of_publish = None
            except:
                year_of_publish = None
            try:
                search_text = str(request.POST['search_text'])
                if search_text == '':
                    search_text = None
            except:
                search_text = None
            if category is not None:
                books_by_magic_word = Book.objects.filter(categories__title__icontains=category)
                for book in books_by_magic_word:
                    books.append(book)
            if search_text is not None:
                books_by_title = Book.objects.filter(title__icontains=search_text)
                for book in books_by_title:
                    books.append(book)
                books_by_authors = Book.objects.filter(authors__full_name__icontains=search_text)
                for book in books_by_authors:
                    books.append(book)
                books_by_interpreters = Book.objects.filter(interpreters__full_name__icontains=search_text)
                for book in books_by_interpreters:
                    books.append(book)
                books_by_publisher = Book.objects.filter(publisher__publisher_name__icontains=search_text)
                for book in books_by_publisher:
                    books.append(book)
                try:
                    search_text = int(search_text)
                    books_by_publish_year = Book.objects.filter(publish_year__exact=search_text)
                    for book in books_by_publish_year:
                        books.append(book)
                except:
                    pass
                books_by_ISBN = Book.objects.filter(ISBN__exact=search_text)
                for book in books_by_ISBN:
                    books.append(book)
                books_by_summery = Book.objects.filter(summery__icontains=search_text)
                for book in books_by_summery:
                    books.append(book)
            context['books'] = set(books)
            return render(request, 'book-filters.html', context)
    else:
        return redirect('accounts:login')


def book_view(request, book_id, book_name):
    context = {}
    if request.user.is_authenticated:

        book = Book.objects.get(id=book_id)
        context['book'] = book

        context['page_title'] = 'کتاب ' + book.title

        BookVisitThread(request, book).start()

        book_number_of_inventory = BookProfile.objects.get(book=book).number_of_inventory
        book_assign_status = UserBookAssign.objects.filter(book=book, date_of_return=None)
        if book_number_of_inventory > book_assign_status.count():
            context['book_is_available_for_loan'] = True

        try:
            user_book_status = UserBookStatus.objects.get(user=request.user, book=book)
            context['is_Wished'] = user_book_status.is_Wished
            context['is_liked'] = user_book_status.is_liked
        except:
            pass
        return render(request, 'book-detail.html', context)
    else:
        return redirect('accounts:login')


def ajax_add_book_to_wish_list(request):
    book_id = request.POST['book_id']
    book = Book.objects.get(id=book_id)
    try:
        user_book_status = UserBookStatus.objects.get(user=request.user, book=book)
        user_book_status.is_Wished = True
        user_book_status.wish_time = jdatetime.datetime.now()
        user_book_status.save()
    except:
        user_book_status = UserBookStatus(
            user=request.user,
            book=book,
            is_Wished=True,
            wish_time=jdatetime.datetime.now(),
        )
        user_book_status.save()
    return JsonResponse({'message': 'ok'})


def ajax_remove_book_from_wish_list(request):
    book_id = request.POST['book_id']
    book = Book.objects.get(id=book_id)
    try:
        user_book_status = UserBookStatus.objects.get(user=request.user, book=book)
        user_book_status.is_Wished = False
        user_book_status.wish_time = None
        user_book_status.save()
    except:
        user_book_status = UserBookStatus(
            user=request.user,
            book=book,
            is_Wished=False,
            wish_time=None,
        )
        user_book_status.save()
    return JsonResponse({'message': 'ok'})


def ajax_add_book_to_liked_list(request):
    book_id = request.POST['book_id']
    book = Book.objects.get(id=book_id)
    try:
        user_book_status = UserBookStatus.objects.get(user=request.user, book=book)
        user_book_status.is_liked = True
        user_book_status.like_time = jdatetime.datetime.now()
        user_book_status.save()
    except:
        user_book_status = UserBookStatus(
            user=request.user,
            book=book,
            is_liked=True,
            like_time=jdatetime.datetime.now(),
        )
        user_book_status.save()
    return JsonResponse({'message': 'ok'})


def ajax_remove_book_from_liked_list(request):
    book_id = request.POST['book_id']
    book = Book.objects.get(id=book_id)
    try:
        user_book_status = UserBookStatus.objects.get(user=request.user, book=book)
        user_book_status.is_liked = False
        user_book_status.like_time = None
        user_book_status.save()
    except:
        user_book_status = UserBookStatus(
            user=request.user,
            book=book,
            is_liked=False,
            like_time=None,
        )
        user_book_status.save()
    return JsonResponse({'message': 'ok'})


class BookVisitThread(threading.Thread):
    def __init__(self, request, book):
        threading.Thread.__init__(self)
        self.request = request
        self.book = book

    def run(self):
        try:
            book_profile = BookProfile.objects.get(book=self.book)
            book_profile.visited_by_users.add(self.request.user)
            book_profile.save()
            return True
        except Exception as e:
            print(str(e))
            return False


def pdf_reader(request, book_id, t):
    context = {}
    if request.user.is_authenticated:
        book = Book.objects.get(id=book_id)
        context['book'] = book
        if str(t) == '0':
            context['type'] = 'demo'
            context['page_title'] = 'مطالعه دموی کتاب ' + book.title
        elif str(t) == '1':
            context['type'] = 'src'
            context['page_title'] = 'مطالعه کامل کتاب ' + book.title
            AddBookToReadingStateThread(request, book).start()
        return render(request, 'book-pdf.html', context)
    else:
        return redirect('accounts:login')


class AddBookToReadingStateThread(threading.Thread):
    def __init__(self, request, book):
        threading.Thread.__init__(self)
        self.request = request
        self.book = book

    def run(self):
        try:
            user_book_status = UserBookStatus.objects.get(user=self.request.user, book=self.book)
            user_book_status.is_reading = True
            user_book_status.reading_started_at = jdatetime.datetime.now()
            user_book_status.save()
            return True
        except Exception as e:
            print(str(e))
            return False


@never_cache
def ajax_pdf_response(request):
    if request.user.is_authenticated:
        book_id = request.POST['book_id']
        print(book_id)
        book = Book.objects.get(id=book_id)
        pdf_file = book.pdf_source.path
        print(pdf_file)
        with open(pdf_file, 'rb') as pdf:
            response = HttpResponse(pdf)
            response["Content-Type"] = 'application/pdf; charset=utf-8'
            response["Content-Disposition"] = 'inline'
            return response
    else:
        return redirect('accounts:login')


def book_audio(request, book_id, book_name=None):
    context = {}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
        book = Book.objects.get(id=book_id)
        context['book'] = book

        context['page_title'] = 'گوش دادن کامل کتاب صوتی ' + book.title
        return render(request, 'book-audio.html', context)
    else:
        return redirect('accounts:login')