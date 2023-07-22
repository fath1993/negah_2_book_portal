import threading
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from accounts.models import UserProfile, UserBookAssign
from bookshelf.models import Book
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from contact.models import AvailableDate, RequestLoan
from website.models import HomePageSliderImage, BooOfTheWeek


def home_view(request):
    context = {}
    if request.user.is_authenticated:
        books = Book.objects.filter(is_published_on_site=True)[:12]
        context['books'] = books
        # featured_books = FeaturedBook.objects.all()
        # context['featured_books'] = featured_books
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
        home_page_slider_images = HomePageSliderImage.objects.filter()
        context['home_page_slider_images'] = home_page_slider_images
        book_of_the_week = BooOfTheWeek.objects.filter()
        context['book_of_the_week'] = book_of_the_week
        if request.method == 'GET':
            return render(request, 'index.html', context)
        else:
            return HttpResponse('not allowed')
    else:
        return redirect('accounts:login')


def loan_request_view(request, book_id):
    context = {}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
        book = Book.objects.get(id=book_id)
        context['book'] = book
        available_dates = AvailableDate.objects.all().order_by('available_date')
        context['available_dates'] = available_dates
        if request.method == 'GET':
            return render(request, 'loan-form.html', context)
        else:
            user = request.user
            book = Book.objects.get(id=book_id)
            date_of_request = request.POST['date']
            hour = request.POST['hour']
            description = request.POST['description']
            print(str(user))
            print(str(date_of_request))
            print(str(hour))
            print(str(description))
            new_request_loan = RequestLoan(
                user=user,
                book=book,
                date_of_request=date_of_request,
                hour=hour,
                description=description,
            )
            new_request_loan.save()
            return redirect('/request-history/')
    else:
        return redirect('accounts:login')


def request_history_view(request):
    context = {}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
        loan_requests = RequestLoan.objects.filter(user=request.user).order_by('-date_of_request')
        context['loan_requests'] = loan_requests
        return render(request, 'my-request.html', context)
    else:
        return redirect('accounts:login')


def remove_request_ajax(request):
    if request.user.is_authenticated:
        user_id = request.POST['user_id']
        user = User.objects.get(id=user_id)
        if user != request.user:
            return HttpResponse('not allowed')
        request_id = request.POST['request_id']
        RequestLoan.objects.get(id=request_id).delete()
        return HttpResponse('ok!')
    else:
        return redirect('accounts:login')


def paginator_creator(request, paginating_object, context):
    page = request.GET.get('page', 1)
    paginator = Paginator(paginating_object, 28)
    try:
        paginating_object = paginator.page(page)
    except PageNotAnInteger:
        paginating_object = paginator.page(1)
    except EmptyPage:
        paginating_object = paginator.page(paginator.num_pages)
    context['books'] = paginating_object


# def categories_view(request):
#     context = {}
#     if request.user.is_authenticated:
#         user_profile = UserProfile.objects.get(user=request.user)
#         context['user_profile'] = user_profile
#         books = Book.objects.filter(is_published_on_site=True).order_by('id')
#         all_categories = Category.objects.all()
#         context['all_categories'] = all_categories
#         if request.method == 'GET':
#             paginator_creator(request, books, context)
#             return render(request, 'category.html', context)
#         elif request.method == 'POST':
#             # publisher = str(request.POST['publisher'])
#             # keyword = str(request.POST['keyword'])
#             # if publisher == 'انتشارات':
#             #     publisher = None
#             # if keyword == 'کلید واژه':
#             #     keyword = None
#
#             try:
#                 mark = str(request.POST['mark'])
#                 if mark == 'بر اساس':
#                     mark = None
#             except:
#                 mark = None
#
#             try:
#                 category = str(request.POST['category'])
#                 if category == 'دسته':
#                     category = None
#             except:
#                 category = None
#             try:
#                 year_of_publish = str(request.POST['year_of_publish'])
#                 if year_of_publish == 'سال انتشار':
#                     year_of_publish = None
#             except:
#                 year_of_publish = None
#             try:
#                 search_text = str(request.POST['search_text'])
#                 if search_text == '':
#                     search_text = None
#             except:
#                 search_text = None
#
#             if category is not None and year_of_publish is None and search_text is None:
#                 books = Book.objects.filter(
#                     Q(is_published_on_site=True) &
#                     Q(categories__category_name__icontains=category)
#                 )
#                 paginator_creator(request, books, context)
#             elif category is not None and year_of_publish is not None and search_text is None:
#                 books = Book.objects.filter(
#                     Q(is_published_on_site=True) &
#                     Q(categories__category_name__icontains=category) &
#                     Q(date_of_publish__icontains=year_of_publish)
#                 )
#                 paginator_creator(request, books, context)
#             elif category is not None and year_of_publish is not None and search_text is not None:
#                 books = Book.objects.filter(
#                     Q(is_published_on_site=True) &
#                     Q(categories__category_name__icontains=category) &
#                     Q(date_of_publish__icontains=year_of_publish) &
#                     Q(title__icontains=search_text) |
#                     Q(summery__icontains=search_text) |
#                     Q(ISBN__icontains=search_text) |
#                     Q(authors__person__person_name__icontains=search_text) |
#                     Q(interpreters__person__person_name__icontains=search_text)
#                 )
#                 paginator_creator(request, books, context)
#             elif category is None and year_of_publish is None and search_text is not None:
#                 books = Book.objects.filter(
#                     Q(is_published_on_site=True) &
#                     Q(title__icontains=search_text) |
#                     Q(summery__icontains=search_text) |
#                     Q(ISBN__icontains=search_text) |
#                     Q(authors__person__person_name__icontains=search_text) |
#                     Q(interpreters__person__person_name__icontains=search_text)
#                 )
#                 paginator_creator(request, books, context)
#             elif search_text is not None and category is not None and year_of_publish is None:
#                 books = Book.objects.filter(
#                     Q(is_published_on_site=True) &
#                     Q(categories__category_name__icontains=category) &
#                     Q(title__icontains=search_text) |
#                     Q(summery__icontains=search_text) |
#                     Q(ISBN__icontains=search_text) |
#                     Q(authors__person__person_name__icontains=search_text) |
#                     Q(interpreters__person__person_name__icontains=search_text)
#                 )
#                 paginator_creator(request, books, context)
#             elif search_text is not None and year_of_publish is not None and category is None:
#                 books = Book.objects.filter(
#                     Q(is_published_on_site=True) &
#                     Q(date_of_publish__icontains=year_of_publish) &
#                     Q(title__icontains=search_text) |
#                     Q(summery__icontains=search_text) |
#                     Q(ISBN__icontains=search_text) |
#                     Q(authors__person__person_name__icontains=search_text) |
#                     Q(interpreters__person__person_name__icontains=search_text)
#                 )
#                 paginator_creator(request, books, context)
#
#             elif year_of_publish is not None and search_text is None and category is None:
#                 books = Book.objects.filter(
#                     Q(is_published_on_site=True) &
#                     Q(date_of_publish__year=year_of_publish)
#                 )
#                 paginator_creator(request, books, context)
#
#             else:
#                 if mark is None:
#                     books = Book.objects.filter(is_published_on_site=True)
#                     print(books)
#                 elif mark == 'دفعات مشاهده':
#                     books = BookVisitedNumber.objects.all().order_by('visited_number')[:40]
#                     context['unusual'] = True
#                 elif mark == 'امتیاز منتقدان':
#                     books = Book.objects.filter(is_published_on_site=True)
#                 elif mark == 'امتیاز کاربران سایت':
#                     books = Book.objects.filter(is_published_on_site=True)
#
#                 paginator_creator(request, books, context)
#             return render(request, 'category.html', context)
#     else:
#         return redirect('accounts:login')


def book_view(request, book_id, book_name):
    context = {}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
        book = Book.objects.get(id=book_id)
        book.visited_by_users.add(request.user)
        book.save()
        BookVisitThread(book).start()
        book_assign_history = UserBookAssign.objects.filter(book=book)
        context['book_is_available_for_loan'] = True
        for book_history in book_assign_history:
            if not book_history.is_this_book_returned:
                context['book_is_available_for_loan'] = False
        context['book'] = book
        tags = book.keywords.all()
        tag_list = []
        for tag in tags:
            tag_list.append(tag.id)
        similar_books = Book.objects.filter()
        context['similar_books'] = similar_books
        return render(request, 'book-page.html', context)
    else:
        return redirect('accounts:login')


class BookVisitThread(threading.Thread):
    def __init__(self, book):
        threading.Thread.__init__(self)
        self.book = book

    def run(self):
        try:
            # number_of_visit = self.book.visited_by_users.all().count()
            # try:
            #     old_book_visited_number = BookVisitedNumber.objects.get(book=self.book)
            #     old_book_visited_number.visited_number = number_of_visit
            #     old_book_visited_number.save()
            #     return True
            # except:
            #     new_book_visited_number = BookVisitedNumber(
            #         book=self.book,
            #         visited_number=number_of_visit,
            #     )
            #     new_book_visited_number.save()
            #     return True
            pass
        except Exception as e:
            print('object is busy. err: ' + str(e), 'd')
            return False


def pdf_reader(request, book_id, t):
    context = {}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
        book = Book.objects.get(id=book_id)
        context['book'] = book
        if t == 0:
            context['type'] = 'demo'
        elif t == 1:
            context['type'] = 'src'
        return render(request, 'book-pdf.html', context)
    else:
        return redirect('accounts:login')


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
        return render(request, 'book-audio.html', context)
    else:
        return redirect('accounts:login')