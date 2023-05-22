from django.shortcuts import render
from app.forms import FindForm
from app.models import Job

# Create your views here.


def home_view(request):
    form = FindForm()
    return render(
        request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []

    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Job.objects.filter(**_filter)

    return render(
        request, 'scraping/list.html', {'object_list': qs, 'form': form})
