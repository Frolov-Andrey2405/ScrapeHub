from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from app.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        """
        The clean function is used to validate the data.
        It's called by the form's is_valid() method, which in turn is called by Django when processing a submitted form.
        The clean function should raise ValidationError if any of its checks fail.
        """
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError(
                    'There is no such user!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('The password is wrong!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError(
                    'This account is disabled')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label='Enter email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Enter your password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Enter your password again',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """
        The clean_password2 function is a custom validation function that checks if the two passwords entered by the user match.
        If they don't, it raises a ValidationError with an error message.
        """
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError(
                "The passwords don't match!")
        return data['password2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name="slug", required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name="slug", required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Specialty'
    )

    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                    label='Receive the newsletter?')

    class Meta:
        model = User
        fields = ('city', 'language', 'send_email')


class ContactForm(forms.Form):
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='City'
    )

    language = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Specialty'
    )

    email = forms.EmailField(
        label='Enter email',
        required=True, widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
