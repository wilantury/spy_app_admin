# Django
from django.urls import path
# Views
from .views import login_view, signup_view

app_name = 'auth'

urlpatterns = [
     path('', login_view, name='login'),
     path('signup', signup_view, name='register')
]
