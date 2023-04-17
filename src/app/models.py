from django.db import models
from app.utils import from_cyrillic_to_eng

# Create your models here.


class City(models.Model):
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
