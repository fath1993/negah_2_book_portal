from django.contrib.auth.models import User
from django.db import models

from bookshelf.models import Book
from django_jalali.db import models as jmodels


class RequestLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                             verbose_name='کاربر درخواست کننده')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کتاب مورد درخواست')
    date_of_request = jmodels.jDateField(null=False, blank=False, editable=True, verbose_name='تاریخ مورد نظر جهت مراجعه و دریافت کتاب')
    date_of_placed_request = jmodels.jDateField(auto_now_add=True, verbose_name='تاریخ ثبت درخواست')
    hour = models.CharField(max_length=255, null=False, blank=False, verbose_name='ساعت مراجعه')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    is_request_processed = models.BooleanField(default=False, null=False, blank=False,
                                               verbose_name='آیا این درخواست رسیدگی شده است؟')

    def __str__(self):
        return str(self.user.username) + ' - ' + str(self.book.title) + ' - ' + str(self.date_of_request)

    class Meta:
        ordering = ['date_of_placed_request', ]
        verbose_name = 'درخواست کتاب'
        verbose_name_plural = 'در خواست های کتاب'


class AvailableDate(models.Model):
    available_date = jmodels.jDateField(null=False, blank=False, editable=True,
                                        verbose_name='تاریخ مجاز مراجعه و دریافت کتاب')
    from_hour = models.CharField(max_length=255, null=False, blank=False, verbose_name='از ساعت')
    to_hour = models.CharField(max_length=255, null=False, blank=False, verbose_name='تا ساعت')

    def __str__(self):
        return str(self.available_date) + ' - از ساعت: ' + str(self.from_hour) + ' - تا ساعت: ' + str(self.to_hour)

    class Meta:
        verbose_name = 'تاریخ و ساعت قابل مراجعه'
        verbose_name_plural = 'تاریخ و ساعت قابل مراجعه'
