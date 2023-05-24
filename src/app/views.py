from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView, ListView, CreateView, UpdateView, DeleteView
)

from .forms import FindForm, VForm
from .models import Job


def home_view(request):
    """
    The home_view function is the main view of the scraping app.
    It renders a form that allows users to enter a URL and scrape it for data.
    The scraped data is then displayed in an HTML table.
    """
    form = FindForm()
    return render(
        request, 'scraping/home.html', {'form': form})


def list_view(request):
    """
    The list_view function is a view that displays the list of jobs.
    It takes in a request and returns an HTML page with the list of jobs.
    """
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Job.objects.filter(**_filter).select_related('city', 'language')
        paginator = Paginator(qs, 10)  # Show 10 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)


def v_detail(request, pk=None):
    """
    The v_detail function is a view that displays the details of a single Job object.
    It takes in an HTTP request and returns an HTML response with the details of the Job object.
    """
    object_ = get_object_or_404(Job, pk=pk)
    return render(request, 'scraping/detail.html', {'object': object_})


class VDetail(DetailView):
    queryset = Job.objects.all()
    template_name = 'scraping/detail.html'


class VList(ListView):
    model = Job
    template_name = 'scraping/list.html'
    form = FindForm()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        The get_context_data function is a method that takes in the context of the view and returns it.
        The context is a dictionary containing all of the data that will be passed to your template.
        In this case, we are adding our form object to the context so it can be rendered by our template.
        """
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form

        return context

    def get_queryset(self):
        """
        The get_queryset function is a method that returns the queryset of objects to be used in this view.
        It takes no arguments, but does have access to self.request which contains all the information about 
        the current request including GET and POST parameters.
        """
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Job.objects.filter(**_filter).select_related(
                'city', 'language')
        return qs


class VCreate(CreateView):
    model = Job
    form_class = VForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')


class VUpdate(UpdateView):
    model = Job
    form_class = VForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')


class VDelete(DeleteView):
    model = Job
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        """
        The get function is used to display a confirmation page before deleting the entry.
        The post function is used to delete the entry.
        """
        messages.success(request, 'Entry successfully deleted.')
        return self.post(request, *args, **kwargs)
