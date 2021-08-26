# Django
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.db.utils import IntegrityError
# Forms
from .forms import LoginForm, SignupForm

Spy = get_user_model()

def logout_view(request):
    logout(request)
    return redirect('auth:login')


def signup_view(request):
    signup_form = SignupForm()
    
    context = {
        "error_msn":None,
        "form":signup_form
    }
    
    if request.method == 'POST':
        signup_form = SignupForm(data=request.POST)
        if signup_form.is_valid():
            email = signup_form.cleaned_data.get('email_address')
            password = signup_form.cleaned_data.get('password')
            re_password = signup_form.cleaned_data.get('re_password')
            if password == re_password:
                try:
                    new_spy = Spy.objects.create_user(email=email, password=password)
                    return redirect('auth:login')
                except IntegrityError:
                    context['error_msn'] = "This email address has been taken already, try a new email."
            else:
                context['error_msn'] = "Your password must match with the re-enter password"


    return render(request, 'auth/signup.html', context)

def login_view(request):

    if request.user.is_authenticated:
        return redirect('spy_app:hits')    
    
    login_form = LoginForm()

    context = {
        "error_msn":None,
        "form":login_form
    }

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
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('spy_app:hits')
            else:
                context['error_msn'] = 'Ups... something went wrong, check your e-mail address and password.'
        else:
            context['error_msn'] = 'Ups... something went wrong.'

    return render(request, 'auth/login.html', context)
