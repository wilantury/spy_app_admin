from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields
from django.forms.widgets import Textarea
# models
from .models import Hit, TeamManager, TeamMembers
# Constants
from .constants import MANAGER, BOSS

Spy = get_user_model()

class ReassignHitForm(forms.Form):
    hitman = forms.ModelChoiceField(queryset=Spy.objects.filter(is_active=True).filter(is_superuser=False))

#https://stackoverflow.com/questions/5329586/django-modelchoicefield-filtering-query-set-and-setting-default-value-as-an-obj
class HitForm(forms.Form):
    target_name = forms.CharField(max_length=150)
    target_location = forms.CharField(max_length=150)
    description = forms.CharField(widget=Textarea())
    hitman_assigned = forms.ModelChoiceField(queryset=Spy.objects.filter(is_superuser=False))
    
    # def _get_hitmans(self):
    #     if self._rol == MANAGER:
    #         team = TeamManager.objects.filter(manager=self._spy.id).first()
    #         if team:
    #             members = TeamMembers.objects.filter(team=team.id)
    #             return members if members else []
    #         return []
    #     elif self._rol == BOSS:
    #         return Spy.objects.filter(is_superuser=False)




    

    