from django.db import models
import jsonfield
from app.utils import from_cyrillic_to_eng


def default_urls():
    return {"work_ua": "", "dou_ua": "", "djinni_co": ""}


class City(models.Model):
    '''
    City model represents a settlement with a name and a slug.
    The slug is automatically generated from the name if not provided.
    '''
    name = models.CharField(
        max_length=100, verbose_name='Name of the settlement', unique=True)
    slug = models.CharField(max_length=100, blank=True, unique=True)

    class Meta:
        verbose_name = 'Name of the settlement'
        verbose_name_plural = 'Name of settlements'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    '''
    Language model represents a programming language with a name and a slug.
    The slug is automatically generated from the name if not provided.
    '''
    name = models.CharField(
        max_length=100, verbose_name='Name of the language', unique=True)
    slug = models.CharField(max_length=100, blank=True, unique=True)

    class Meta:
        verbose_name = 'Name of the language'
        verbose_name_plural = 'Name of languages'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Job(models.Model):
    '''
    Job model represents a job posting with a URL, title, company, description,
    city, programming language, and time stamp.
    '''
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Job Title ')
    company = models.CharField(max_length=250, verbose_name='Company')
    description = models.TextField(verbose_name='Job Description ')
    city = models.ForeignKey(
        'City', on_delete=models.CASCADE, verbose_name='City')
    language = models.ForeignKey(
        'Language', on_delete=models.CASCADE,
        verbose_name='Programming Language')
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-time_stamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    '''Error model represents an error occurrence'''
    time_stamp = models.DateTimeField(auto_now_add=True)
    data = jsonfield.JSONField()

    def __str__(self):
        return str(self.time_stamp)


class Url(models.Model):
    '''Model representing a URL.'''
    city = models.ForeignKey(
        'City', on_delete=models.CASCADE, verbose_name='City')
    language = models.ForeignKey(
        'Language', on_delete=models.CASCADE,
        verbose_name='Programming Language')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language")
