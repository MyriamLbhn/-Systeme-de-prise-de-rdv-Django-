from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usersapp.forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def home(request):
	""" Renders the 'home.html' template, the home page of the website.

    Args:
        request (HttpRequest): An object representing the current request.

    Returns:
        HttpResponse: A response object that renders the 'home.html' template.

    """
	return render(request, 'usersapp/home.html')


def login_view(request):
    """Render the 'login.html' template for user authentication.

    Args:
        request (HttpRequest): An object representing the current request.

    Returns:
        HttpResponse: A response object that renders the 'login.html' template.

    """
    return render(request, 'usersapp/login.html')

def logout_view(request):
    """Log out the current user and render the 'logout.html' template.

    Args:
        request (HttpRequest): An object representing the current request.

    Returns:
        HttpResponse: A response object that renders the 'logout.html' template.

    """
    return render(request, 'usersapp/logout.html')

def register(request):
    """Register a new user,log them in if the submitted form is valid and redirect them to the home page.

    Args:
        request (HttpRequest): An object representing the current request.

    Returns:
        HttpResponse: A response object that renders the 'inscription.html' template with the user registration form.

    """
    if request.method == 'POST' :
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()		
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)	
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')					
            return redirect('home')
    else :
        form = UserRegistrationForm()
    return render(request,'usersapp/register.html',{'form' : form})

@login_required
def profil(request):
    """Display the user's profile page and allow them to edit their profile information.

    Args:
        request (HttpRequest): An object representing the current request.

    Returns:
        HttpResponse: A response object that renders the 'profil.html' template with the user's profile information.

    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profil.html', {'form': form})


