from django.db import models
from django_jalali.db import models as jmodel


class FileGallery(models.Model):
    file_alt = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام فایل')
    file_src = models.FileField(upload_to='files', null=False, blank=False, verbose_name='سورس فایل')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.file_alt

    class Meta:
        verbose_name = 'گالری فایل'
        verbose_name_plural = 'گالری فایل ها'
