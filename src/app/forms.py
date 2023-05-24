from django import forms
from app.models import City, Language, Job


class FindForm(forms.Form):

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City')

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Programming Language')


class VForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Specialty'
    )
    url = forms.CharField(label='URL', widget=forms.URLInput(
        attrs={'class': 'form-control'}))
    title = forms.CharField(label='Job Title', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    company = forms.CharField(label='The company', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(
        label='Job Description',
        widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Job
        fields = '__all__'
