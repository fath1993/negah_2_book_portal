from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from bookshelf.models import Book
import threading
from django_jalali.db import models as jmodels


class Message(models.Model):
    message = models.TextField(null=False, blank=False, verbose_name='اطلاعیه')
    time = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    def __str__(self):
        return self.message[:100]

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'


class Notification(models.Model):
    notification = models.ForeignKey(Message, on_delete=models.CASCADE, null=False, blank=False, verbose_name='اطلاعیه')

    def __str__(self):
        return self.notification.message[:100]

    class Meta:
        ordering = ['-notification__time', ]
        verbose_name = 'اطلاعیه'
        verbose_name_plural = 'اطلاعیه ها'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        users = User.objects.all()
        notification = Notification.objects.get(id=self.id)
        SendNotificationThread('public', users, notification).start()
        super().save(*args, **kwargs)


class PrivateMessage(models.Model):
    users = models.ManyToManyField(User, verbose_name='کاربران دریافت کننده پیام')
    private_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=False, blank=False, verbose_name='پیام شخصی')

    def __str__(self):
        return self.private_message.message[:100]

    class Meta:
        verbose_name = 'پیام شخصی'
        verbose_name_plural = 'پیام های شخصی'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        users = self.users.all()
        private_message = PrivateMessage.objects.get(id=self.id)
        SendNotificationThread('personal', users, private_message).start()
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کاربر')
    profile_image = models.ImageField(upload_to='user_profile_pic', null=True, blank=True, verbose_name='عکس پروفایل')
    notification_box = models.ManyToManyField(Notification, blank=True, verbose_name='اطلاعیه ها')
    is_notification_seen = models.BooleanField(default=False, null=False, blank=False, verbose_name='آیا نوتیفیکیشن ها خوانده شد؟')
    message_box = models.ManyToManyField(PrivateMessage, blank=True, verbose_name='پیام ها')
    is_message_seen = models.BooleanField(default=False, null=False, blank=False, verbose_name='آیا پیام ها خوانده شد؟')
    specific_book_only_for_this_user = models.ManyToManyField(Book, related_name='specific_book_only_for_this_user', verbose_name='کتاب های خاص این کاربر')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'


@receiver(post_save, sender=User)
def auto_create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class SendNotificationThread(threading.Thread):
    def __init__(self, message_type, users, message_model):
        threading.Thread.__init__(self)
        self.message_type = message_type
        self.users = users
        self.message_model = message_model

    def run(self):
        if self.message_type == 'public':
            for user in self.users:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.notification_box.add(self.message_model)
                user_profile.is_notification_seen = False
                user_profile.save()
        elif self.message_type == 'personal':
            for user in self.users:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.message_box.add(self.message_model)
                user_profile.is_message_seen = False
                user_profile.save()


class UserBookStatus(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, editable=False, on_delete=models.CASCADE, verbose_name='کاربر')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False, editable=False, verbose_name='کتاب')
    is_reading = models.BooleanField(default=False, editable=False, verbose_name='آیا کتاب در حال مطالعه است؟')
    last_page = models.PositiveIntegerField(default=0, null=False, blank=False, editable=False, verbose_name='آخرین صفحه مطالعه شده')
    is_finished = models.BooleanField(default=False, editable=False, verbose_name='آیا خواندن کتاب پایان یافته است؟')
    finish_time = jmodels.jDateTimeField(null=True, blank=True, editable=False, verbose_name='تاریخ پایان مطالعه کتاب')
    is_Wished = models.BooleanField(default=False, editable=False, verbose_name='آیا کتاب در لیست مطالعه ی آتی است؟')
    wish_time = jmodels.jDateTimeField(null=True, blank=True, editable=False, verbose_name='تاریخ اضافه شدن به لیست مطالعه اتی')
    is_liked = models.BooleanField(default=False, editable=False, verbose_name='آیا کتاب جزو موارد مورد علاقه است؟')
    like_time = jmodels.jDateTimeField(null=True, blank=True, editable=False, verbose_name='تاریخ اضافه شدن به لیست علاقه مندی ها')

    def __str__(self):
        return self.user.username + ' | ' + self.book.title

    class Meta:
        verbose_name = 'وضعیت کتاب کاربر'
        verbose_name_plural = 'وضعیت کتاب های کاربران'


class UserBookAssign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کاربر')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کتاب')
    date_of_assignment = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ واگذاری')
    date_of_return = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ بازگرداندن')

    def __str__(self):
        return self.book.title + " | " + self.user.username

    class Meta:
        verbose_name = 'واگذاری'
        verbose_name_plural = 'واگذاری ها'
