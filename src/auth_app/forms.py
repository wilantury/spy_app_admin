from django import forms

class LoginForm(forms.Form):
    email_address = forms.EmailField(help_text="Email address", label="Email", max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)

class SignupForm(LoginForm):
    re_password = forms.CharField(widget=forms.PasswordInput, label="Re-enter Password", required=True)
