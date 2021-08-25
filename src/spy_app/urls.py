from django.urls import path
# Views
from .views import hits_view

app_name = 'spy_app'

urlpatterns = [
    path('hits', hits_view, name='hits')
]
