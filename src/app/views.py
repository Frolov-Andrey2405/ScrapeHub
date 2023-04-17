from django.shortcuts import render
from app.models import Job

# Create your views here.


def home_view(request):
    qs = Job.objects.all()
    return render(request, 'home.html', {'object_list': qs})
