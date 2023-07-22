from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from accounts.models import UserProfile
from bookshelf.models import Book
from contact.models import RequestLoan, AvailableDate


def login_view(request):
    context = {'page_title': 'صفحه ورود'}
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('bookshelf:home')
        else:
            return render(request, 'accounts/sign-in.html', context)
    else:
        if request.user.is_authenticated:
            return redirect('bookshelf:home')
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bookshelf:home')
            else:
                context['err'] = 'نام کاربری یا کلمه عبور صحیح نمی باشد'
                return render(request, 'accounts/sign-in.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:login')


def signup_view(request):
    context = {'page_title': 'صفحه ثبت نام'}
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('bookshelf:home')
        else:
            return render(request, 'accounts/sign-up.html', context)
    else:
        if request.user.is_authenticated:
            return redirect('bookshelf:home')
        else:
            phone_number = request.POST['phone-number']
            email = request.POST['email']
            full_name = request.POST['full-name']
            password_1 = request.POST['password-1']
            password_2 = request.POST['password-2']

            if phone_number is None:
                context['err'] = 'شماره همراه صحیح نمی باشد'
                return render(request, 'accounts/sign-up.html', context)
            else:
                try:
                    user = User.objects.get(username=phone_number)
                    context['err'] = 'شماره همراه در سامانه موجود می باشد'
                    return render(request, 'accounts/sign-up.html', context)
                except:
                    pass

            if password_1 != password_2:
                context['err'] = 'کلمات عبور وارد شده یکسان نمی باشند'
                return render(request, 'accounts/sign-up.html', context)


            new_user = User.objects.create_user(username=phone_number, email=email, first_name=full_name,
                                                password=password_1, is_active=True)
            login(request, new_user)
            return redirect('bookshelf:home')


def profile_view(request):
    context = {'page_title': 'پروفایل کاربری'}
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_profile = UserProfile.objects.get(user=request.user)
            context['user_profile'] = user_profile
            return render(request, 'profile.html', context)
        else:
            pass
    else:
        return redirect('accounts:login')


def personal_library(request):
    context = {'page_title': 'کتاب خانه من'}
    if request.user.is_authenticated:
        return render(request, 'personal-library.html', context)
    else:
        return redirect('accounts:login')


def loan_request_view(request, book_id):
    context = {'page_title': 'درخواست امانت فیزیکی کتاب'}
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_profile = UserProfile.objects.get(user=request.user)
            context['user_profile'] = user_profile
            book = Book.objects.get(id=book_id)
            context['book'] = book
            available_dates = AvailableDate.objects.all().order_by('available_date')
            context['available_dates'] = available_dates
            return render(request, 'book-request-loan.html', context)
        else:
            book = Book.objects.get(id=book_id)
            date_of_request = request.POST['date']
            hour = request.POST['hour']
            description = request.POST['description']
            new_request_loan = RequestLoan(
                user=request.user,
                book=book,
                date_of_request=date_of_request,
                hour=hour,
                description=description,
            )
            new_request_loan.save()
            return redirect('accounts:request-history')
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


def request_history_view(request):
    context = {'page_title': 'سوابق درخواست ها'}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
        loan_requests = RequestLoan.objects.filter(user=request.user).order_by('-date_of_request')
        context['loan_requests'] = loan_requests
        return render(request, 'my-request.html', context)
    else:
        return redirect('accounts:login')


@never_cache
def ajax_add_book_to_profile(request):
    if request.user.is_authenticated:
        try:
            print(0)
            book_id = request.POST['book_id']
            print(book_id)
            book = Book.objects.get(id=book_id)
            user_profile = UserProfile.objects.get(user=request.user)
            try:
                old_reading_book = user_profile.reading_book.get(user=request.user, book=book)
                old_reading_book.last_page = 0
                old_reading_book.save()
                print('old_reading_book')
            except Exception as e:
                # new_reading_book = BookReadingHistory(
                #     user=request.user,
                #     book=book,
                # )
                # new_reading_book.save()
                # user_profile.reading_book.add(new_reading_book)
                user_profile.save()
                print('new_reading_book')
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e))
        return HttpResponse('Ok')
    else:
        return redirect('accounts:login')


@never_cache
def ajax_remove_book_from_profile(request):
    if request.user.is_authenticated:
        book_id = request.POST['book_id']
        print(book_id)
        book = Book.objects.get(id=book_id)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.reading_book.get(user=request.user, book=book).delete()
        user_profile.save()
        return HttpResponse('Ok')
    else:
        return redirect('accounts:login')


@never_cache
def ajax_add_notification_to_read_group(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.is_notification_seen = True
        user_profile.save()
        return HttpResponse('Ok')
    else:
        return redirect('accounts:login')


@never_cache
def ajax_add_message_to_read_group(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.is_message_seen = True
        user_profile.save()
        return HttpResponse('Ok')
    else:
        return redirect('accounts:login')