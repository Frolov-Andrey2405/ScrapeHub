from django.shortcuts import render
from app.models import Job

# Create your views here.


def home_view(request):
    qs = Job.objects.all()
    return render(request, 'scraping/home.html', {'object_list': qs})
