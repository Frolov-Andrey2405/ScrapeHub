from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        """
        The clean function is used to validate the data.
        It's called by Django when you call form.is_valid().
        If it raises a ValidationError, then is_valid() will return False.
        """
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)

            if not qs.exists():
                raise forms.ValidationError('There is no such user!')

            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль не верный!')

            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('This account is disabled')

        return super(UserLoginForm, self).clean(*args, **kwargs)
