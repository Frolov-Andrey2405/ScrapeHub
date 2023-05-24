import datetime as dt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from accounts.forms import (
    UserLoginForm, UserRegistrationForm, UserUpdateForm, ContactForm
)

from app.models import Error

User = get_user_model()


def login_view(request):
    """
    The login_view function is a view that allows users to login.
    It takes in the request and returns a rendered template of the login page.
    If the form is valid, it will authenticate and log in the user.
    """
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    The logout_view function logs the user out of their account and redirects them to the home page.
    """
    logout(request)
    return redirect('home')


def register_view(request):
    """
    The register_view function is used to register a new user.
    It takes the request as an argument and returns a rendered template.
    The function first creates an instance of the UserRegistrationForm class, which is imported from forms.py in this app's directory, and passes it to the template context as form. If there are no errors in validation, then we save the form data into a new_user variable without committing it yet (commit=False). We then set that user's password using set_password() method provided by Django for hashing passwords before saving them into database; otherwise they would be stored in plain text format which would be
    """
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(
            request, 'The user has been added to the system.')
        return render(
            request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    """
    The update_view function is used to update the user's profile information.
    The function first checks if the user is authenticated, and if so, it creates a UserUpdateForm object with initial data from the database.
    If there are POST requests (i.e., when a form has been submitted), then we check whether or not that form is valid and save its cleaned data in variables for later use.
    We then update our database with this new information by setting each field equal to its respective variable value before saving it all at once using .save().  We also send a success message to let users know their changes have been saved.
    """
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'The data is saved.')
                return redirect('accounts:update')

        form = UserUpdateForm(
            initial={
                'city': user.city,
                'language': user.language,
                'send_email': user.send_email
            })

        return render(request, 'accounts/update.html', {
            'form': form,
            'contact_form': contact_form
        })

    else:
        return redirect('accounts:login')


def delete_view(request):
    """
    The delete_view function is a view that allows the user to delete their account.
    It first checks if the user is authenticated, and then it gets the current logged in user.
    If there's a POST request, it deletes that specific User object from the database.

    """
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'User deleted :(')
    return redirect('home')


def contact(request):
    """
    The contact function is used to send data from the contact form to the database.
    The function checks if a POST request has been made, and if so, it creates a ContactForm object with the POST data.
    If this form is valid (i.e., all fields are filled in correctly), then it gets cleaned_data from that form and saves 
    that information into variables city, language and email. It then checks whether there already exists an Error object 
    for today's date in the database; if so, it appends new user_data to its existing list of user_data; otherwise, it
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append(
                    {'city': city, 'email': email, 'language': language})
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [
                    {'city': city, 'email': email, 'language': language}
                ]}
                Error(data=data).save()
            messages.success(
                request, 'Data has been sent to the administration.')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')
