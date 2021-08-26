from django.urls import path
# Views
from .views import hits_view, hit_detail, hit_create

app_name = 'spy_app'

urlpatterns = [
    path('hits', hits_view, name='hits'),
    path('hits/create', hit_create, name='hit_create'),
    path('hits/<pk>', hit_detail, name='hit_detail'),
]
