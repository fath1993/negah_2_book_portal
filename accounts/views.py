import re
import jdatetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from text_unidecode import unidecode

from accounts.models import UserProfile, UserBookStatus, Message, UserBookAssign
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
        user_book_status = UserBookStatus.objects.filter(user=request.user)
        context['reading_books'] = user_book_status.filter(is_reading=True)
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


def ajax_remove_book_from_reading_state(request):
    if request.user.is_authenticated:
        book_id = request.POST['book_id']
        book = Book.objects.get(id=book_id)
        user_book_status = UserBookStatus.objects.get(user=request.user, book=book)
        user_book_status.is_reading = False
        user_book_status.save()
        return JsonResponse({'message': 'ok'})
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


def ajax_user_message_state(request):
    messages = Message.objects.filter(users__exact=request.user)[:5]
    json_response_body = {
        'is_message_seen': request.user.userprofile.is_message_seen,
        'message_has_seen_at': str(request.user.userprofile.message_has_seen_at),

    }

    messages_dict = {}
    i = 0
    for message in messages:
        messages_dict[i] = {
            'content': message.content,
            'created_at': str(message.created_at.strftime('%Y-%m-%d %H:%M'))
        }
        i += 1
    json_response_body['messages'] = messages_dict
    return JsonResponse(json_response_body)


def user_report_view(request):
    context = {'page_title': 'گزارشات آماری'}
    if request.user.is_authenticated:
        context['custom_range'] = False
        if request.method == 'GET':
            context['today'] = jdatetime.datetime.now().date()
            users = User.objects.all()
            users_book_assign = UserBookAssign.objects.all()
            user_book_status = UserBookStatus.objects.all()

            now = jdatetime.datetime.now()
            this_year = now.year
            this_month = now.month
            user_book_report = []
            date_form = jdatetime.datetime(year=this_year, month=1, day=1)
            for user in users:
                if 1 < this_month < 3:
                    user_book_report.append([user, users_book_assign.filter(user=user,
                                                                            date_of_assignment__range=[
                                                                                date_form,
                                                                                now]).count(), '-',
                                             '-', '-', user_book_status.filter(user=user,
                                                                               reading_started_at__range=[
                                                                                   date_form,
                                                                                   now]).count(), '-',
                                             '-', '-'])


                elif 3 < this_month < 6:
                    date_3_month_to = jdatetime.datetime(year=this_year, month=3, day=31)
                    user_book_report.append([user, users_book_assign.filter(user=user,
                                                                            date_of_assignment__range=[
                                                                                date_form,
                                                                                date_3_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          now]).count(),
                                             '-', '-', user_book_status.filter(user=user,
                                                                               reading_started_at__range=[
                                                                                   date_form,
                                                                                   date_3_month_to]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         now]).count(),
                                             '-', '-'])

                elif 6 < this_month < 9:
                    date_3_month_to = jdatetime.datetime(year=this_year, month=3, day=31)
                    date_6_month_to = jdatetime.datetime(year=this_year, month=6, day=31)
                    user_book_report.append([user, users_book_assign.filter(user=user,
                                                                            date_of_assignment__range=[
                                                                                date_form,
                                                                                date_3_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          date_6_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          now]).count(), '-',
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         date_3_month_to]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         date_6_month_to]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         now]).count()
                                                , '-'])


                elif 9 < this_month < 12:
                    date_3_month_to = jdatetime.datetime(year=this_year, month=3, day=31)
                    date_6_month_to = jdatetime.datetime(year=this_year, month=6, day=31)
                    date_9_month_to = jdatetime.datetime(year=this_year, month=9, day=30)
                    user_book_report.append([user, users_book_assign.filter(user=user,
                                                                            date_of_assignment__range=[
                                                                                date_form,
                                                                                date_3_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          date_6_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          date_9_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          now]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         date_3_month_to]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         date_6_month_to]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         date_9_month_to]).count()
                                                , user_book_status.filter(user=user,
                                                                          reading_started_at__range=[
                                                                              date_form,
                                                                              now]).count()])




                elif this_month == 12:
                    date_3_month_to = jdatetime.datetime(year=this_year, month=3, day=31)
                    date_6_month_to = jdatetime.datetime(year=this_year, month=6, day=31)
                    date_9_month_to = jdatetime.datetime(year=this_year, month=9, day=30)
                    date_12_month_to = jdatetime.datetime(year=this_year, month=12, day=30)
                    user_book_report.append([user, users_book_assign.filter(user=user,
                                                                            date_of_assignment__range=[
                                                                                date_form,
                                                                                date_3_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          date_6_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          date_9_month_to]).count(),
                                             users_book_assign.filter(user=user,
                                                                      date_of_assignment__range=[
                                                                          date_form,
                                                                          date_12_month_to]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         date_3_month_to]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         date_6_month_to]).count(),
                                             user_book_status.filter(user=user,
                                                                     reading_started_at__range=[
                                                                         date_form,
                                                                         date_9_month_to]).count()
                                                , user_book_status.filter(user=user,
                                                                          reading_started_at__range=[
                                                                              date_form,
                                                                              date_12_month_to]).count()])

                context['user_book_report'] = user_book_report
        else:
            context['custom_range'] = True
            from_date = request.POST['from-date']
            to_date = request.POST['to-date']
            context['from_date'] = from_date
            context['to_date'] = to_date
            try:
                print(date_extractor(from_date))
                print(date_extractor(to_date))
            except Exception as e:
                print('except' + str(e))
            users = User.objects.all()
            users_book_assign = UserBookAssign.objects.all()
            user_book_status = UserBookStatus.objects.all()
            user_book_report = []
            for user in users:
                user_book_report.append([user, users_book_assign.filter(user=user,
                                                                        date_of_assignment__range=[
                                                                            from_date,
                                                                            to_date]).count(),
                                         user_book_status.filter(user=user,
                                                                 reading_started_at__range=[
                                                                     from_date,
                                                                     to_date]).count()])

            context['user_book_report'] = user_book_report
        return render(request, 'user-report.html', context)
    else:
        return redirect('accounts:login')


def date_extractor(string):
    to_standard_unicode = unidecode(string)
    string_date = re.findall(r'(\d+-\d+-\d+)', to_standard_unicode)
    remove_slash = string_date[0].replace("-", " ")
    separation = remove_slash.split()
    year = separation[0]
    month = separation[1]
    day = separation[2]
    return jdatetime.date(year=int(year), month=int(month), day=int(day))
