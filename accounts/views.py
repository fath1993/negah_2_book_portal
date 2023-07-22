from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from accounts.models import UserProfile
from bookshelf.models import Book


def login_view(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'accounts/sign-in.html')

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'accounts/sign-in.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('accounts:login')
    else:
        return redirect('bookshelf:home')


def signup_view(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('bookshelf:home')
        else:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            new_user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                last_name=last_name, password=password, is_active=True)
            login(request, new_user)
            return redirect('bookshelf:home')

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('bookshelf:home')
        else:
            return render(request, 'accounts/sign-up.html')


def personal_library(request):
    context = {}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
        return render(request, 'personal-library.html', context)
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