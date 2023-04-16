from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Name of the settlement')
    slug = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Name of the settlement'
        verbose_name_plural = 'Name of settlements'

    def __str__(self):
        return self.name
