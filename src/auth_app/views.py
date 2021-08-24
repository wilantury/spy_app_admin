# Django
from django.shortcuts import render
from django.contrib.auth import authenticate, login
# Forms
from .forms import LoginForm, SignupForm


def signup_view(request):
    signup_form = SignupForm()

    context = {
        "form":signup_form
    }
    return render(request, 'auth/signup.html', context)

def login_view(request):

    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email_address')
            password = login_form.cleaned_data.get('password')
            spy = authenticate(email=email, password=password)
            print(spy)
            if spy is not None:
                login(request, spy)
                if spy.is_staff and spy.is_superuser: # Boss
                    print("Superuser")
                elif spy.is_staff and not spy.is_superuser: # manager
                    print("Manager")
                elif not spy.is_staff and not spy.is_superuser: # hitman
                    print("Hitman")

    context = {
        "form":login_form
    }
    return render(request, 'auth/login.html', context)
