from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from tinymce import models as tinymce_models

from file_gallery.models import FileGallery

LANGUAGE = (('فارسی', 'فارسی'), ('انگلیسی', 'انگلیسی'))
BOOK_INVOLVED_PERSON_ROLE = (('نویسنده', 'نویسنده'), ('سرشناسه', 'سرشناسه'), ('مترجم', 'مترجم'), ('پدید آورنده', 'پدید آورنده'),
                             ('گوینده', 'گوینده'), ('سایر', 'سایر'))
MAGIC_WORDS = (('category', 'category'), ('keyword', 'keyword'), ('subject', 'subject'))
CLASSIFICATION = (('دیویی', 'دیویی'), ('کنگره', 'کنگره'))


class BookInvolvedPerson(models.Model):
    full_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام کامل')
    images = models.ManyToManyField(FileGallery, blank=True, verbose_name='تصاویر')
    role = models.CharField(max_length=255, choices=BOOK_INVOLVED_PERSON_ROLE, null=False, blank=False, verbose_name='نقش')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'دست اندر کار کتاب'
        verbose_name_plural = 'دست اندر کاران کتاب'



class MagicWord(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    slug_title = models.CharField(max_length=255, null=False, blank=False, editable=False, verbose_name='اسلاگ عنوان')
    word_type = models.CharField(max_length=255,choices=MAGIC_WORDS, null=False, blank=False, verbose_name='نوع کلمه')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کلمه جادویی'
        verbose_name_plural = 'کلمات جادویی'

    def save(self, *args, **kwargs):
        self.slug_title = slug_generator(self.title)
        super().save(*args, **kwargs)


class Publisher(models.Model):
    publisher_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام انتشارات')
    publisher_address = models.CharField(max_length=255, null=False, blank=False, verbose_name='ادرس')

    def __str__(self):
        return self.publisher_name + " - " + self.publisher_address

    class Meta:
        verbose_name = 'انتشارات'
        verbose_name_plural = 'انتشارات'


class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    authors = models.ManyToManyField(BookInvolvedPerson, related_name='book_involved_person_authors', blank=True, verbose_name='سرشناسگان')
    interpreters = models.ManyToManyField(BookInvolvedPerson, related_name='book_involved_person_interpreters', blank=True, verbose_name='پدیدآورندگان')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ناشر')
    publish_place = models.CharField(max_length=255, null=True, blank=True, verbose_name='مکان نشر')
    publish_year = models.PositiveIntegerField(null=True, blank=True, verbose_name='سال نشر')
    date_of_publish = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ فهرست نویسی')
    language = models.CharField(choices=LANGUAGE, max_length=255, null=True, blank=True, verbose_name='زبان')
    ISBN = models.CharField(max_length=255, null=True, blank=True, verbose_name='شابک')
    subjects = models.ManyToManyField(MagicWord, related_name='magic_word_subjects', blank=True, verbose_name='موضوعات')
    categories = models.ManyToManyField(MagicWord, related_name='magic_word_categories', blank=True, verbose_name='دسته ها')
    keywords = models.ManyToManyField(MagicWord, related_name='magic_word_keywords', blank=True, verbose_name='کلمات کلیدی')
    classification = models.CharField(max_length=255, choices=CLASSIFICATION, null=True, blank=True, verbose_name='رده بندی')
    registration_number = models.PositiveIntegerField(null=True, blank=True, verbose_name='شماره ثبت')
    version = models.PositiveIntegerField(null=True, blank=True, verbose_name='شماره نسخه')
    on_paper_image = models.OneToOneField(FileGallery, related_name='on_paper_image', null=True, blank=True,
                                          on_delete=models.SET_NULL, verbose_name='تصویر جلد کتاب')
    book_images = models.ManyToManyField(FileGallery, related_name='book_images', blank=True, verbose_name='سایر تصاویر مرتبط به کتاب')
    summery = models.TextField(null=True, blank=True, verbose_name='خلاصه')
    number_of_pages = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='تعداد صفحات کتاب')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.title + " - " + self.summery[:30]

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'


class BookProfile(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, null=False, blank=False, editable=False, verbose_name='کتاب')

    pdf_demo = models.FileField(upload_to='pdf_demo', null=True, blank=True, verbose_name='فایل دموی نوشتاری انلاین')
    pdf_source = models.FileField(upload_to='pdf_source', null=True, blank=True,
                                  verbose_name='فایل نوشتاری کامل انلاین')
    audio_demo = models.OneToOneField(FileGallery, related_name='audio_demo', on_delete=models.SET_NULL, null=True,
                                      blank=True,
                                      verbose_name='فایل دموی صوتی')
    audio_source = models.ManyToManyField(FileGallery, blank=True, related_name='audio_source',
                                          verbose_name='فایل های کامل صوتی')
    audio_speaker = models.ForeignKey(BookInvolvedPerson, related_name='book_involved_person_audio_speaker',
                                      on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='نام گوینده صوتی')
    review = tinymce_models.HTMLField(null=True, blank=True, verbose_name='نقد و بررسی')
    visited_by_users = models.ManyToManyField(User, blank=True, related_name='visited_by_users', verbose_name='کاربر های مشاهده کننده')
    number_of_inventory = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name='تعداد نسخ موجود تحت تملک کتابخانه')
    is_published_on_site = models.BooleanField(default=False, verbose_name='آیا کتاب در سایت ارائه شود؟')

    def __str__(self):
        return self.book.title

    class Meta:
        verbose_name = 'پروفایل کتاب'
        verbose_name_plural = 'پروفایل کتاب ها'


@receiver(post_save, sender=Book)
def book_profile_creator(sender, instance, **kwargs):
    try:
        book_profile = BookProfile.objects.get(book=instance)
    except:
        new_book_profile = BookProfile(
            book=instance
        )
        new_book_profile.save()


def slug_generator(word_str):
    word_str = str(word_str)
    word_str = word_str.replace('ي', 'ی')
    word_str = word_str.replace('آ', 'ا')
    word_str = word_str.replace('(', ' ')
    word_str = word_str.replace(')', ' ')
    word_str = word_str.replace('.', ' ')
    word_str = word_str.replace('..', ' ')
    word_str = word_str.replace(',', ' ')
    word_str = word_str.replace(',,', ' ')
    word_str = word_str.replace('|', ' ')
    word_str = word_str.replace('||', ' ')
    word_str = word_str.replace('?', ' ')
    word_str = word_str.replace('??', ' ')
    word_str = word_str.replace('!', ' ')
    word_str = word_str.replace('!!', ' ')
    word_str = word_str.replace('/', ' ')
    word_str = word_str.replace('//', ' ')
    word_str = word_str.replace('\\', ' ')
    word_str = word_str.replace('        ', ' ')
    word_str = word_str.replace('       ', ' ')
    word_str = word_str.replace('      ', ' ')
    word_str = word_str.replace('     ', ' ')
    word_str = word_str.replace('    ', ' ')
    word_str = word_str.replace('   ', ' ')
    word_str = word_str.replace('  ', ' ')
    word_str = word_str.replace(' ', '-')
    return word_str