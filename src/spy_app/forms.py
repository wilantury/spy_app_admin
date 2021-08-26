from django import forms
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.forms import fields

Spy = get_user_model()

class ReassignHitForm(forms.Form):
    hitman = forms.ModelChoiceField(queryset=Spy.objects.filter(is_active=True).filter(is_superuser=False))