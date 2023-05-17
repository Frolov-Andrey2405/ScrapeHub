from django.contrib import admin
from app.models import City, Language, Job, Error


# Register your models here.

admin.site.register(City)
admin.site.register(Language)
admin.site.register(Job)
admin.site.register(Error)
