# Django
from django.urls import path
# Views
from .views import login_view, signup_view, logout_view

app_name = 'auth'

urlpatterns = [
     path('', login_view, name='login'),
     path('logout', logout_view, name='logout'),
     path('register', signup_view, name='register')
]
