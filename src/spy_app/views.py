from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
# Models
from .models import Hit

@login_required
def hits_view(request):
    spy = request.user

    hitmans_hits = Hit.objects.filter(hitman_assigned=spy.id)
    context = {
        'hits':hitmans_hits
    }


    if spy.is_staff and spy.is_superuser: # Boss
        print("Superuser view")
    elif spy.is_staff and not spy.is_superuser: # manager
        return render(request, 'hits/manager_hits.html', context)
    elif not spy.is_staff and not spy.is_superuser: # hitman
        return render(request, 'hits/hitman_hits.html', context)