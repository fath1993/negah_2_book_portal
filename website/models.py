from django.contrib.auth.models import User
from django.db import models

from bookshelf.models import Book


class HomePageSliderImage(models.Model):
    order_id = models.PositiveSmallIntegerField(default=0, null=False, blank=False, verbose_name='اولویت نمایش')
    image = models.ImageField(upload_to='main page slider', null=False, blank=False, verbose_name='بنر صفحه اصلی')

    def __str__(self):
        return self.image.name

    class Meta:
        ordering = ['order_id', ]
        verbose_name = 'بنر صفحه اصلی'
        verbose_name_plural = 'بنر صفحه اصلی'


class BooOfTheWeek(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کتاب')

    def __str__(self):
        return self.book.title

    class Meta:
        verbose_name = 'کتاب هفته'
        verbose_name_plural = 'کتاب های هفته'


class FeaturedBook(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کتاب')

    def __str__(self):
        return self.book.title

    class Meta:
        verbose_name = 'کتاب ویژه'
        verbose_name_plural = 'کتاب های ویژه'