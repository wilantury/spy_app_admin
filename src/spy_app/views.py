from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# utils
from .utils import get_context
from .constants import HITMAN, MANAGER

@login_required
def hits_view(request):
    spy = request.user
    if spy.is_staff and spy.is_superuser: # Boss
        print("Superuser view")
    elif spy.is_staff and not spy.is_superuser: # manager
        context = get_context(spy, MANAGER)          
        return render(request, 'hits/manager_hits.html', context)
    elif not spy.is_staff and not spy.is_superuser: # hitman
        context = get_context(spy, HITMAN)            
        return render(request, 'hits/hitman_hits.html', context)