from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
# utils
from .utils import get_context, get_hitmans
from .constants import FAILED, HITMAN, MANAGER, BOSS, COMPLETED
# Models
from .models import Hit, HitStatus
# Forms
from .forms import ReassignHitForm, HitForm

Spy = get_user_model()

@login_required
@permission_required('spy_app.can_create_hit')
def hit_create(request):
    spy = request.user
    rol = None
    hit_form = HitForm(request.POST or None)

    if request.method == "POST":
         if hit_form.is_valid():
            data_form = hit_form.cleaned_data
            target_name = data_form.get('target_name')
            target_location = data_form.get('target_location')
            description = data_form.get('description')
            hitman_assigned = data_form.get('hitman_assigned')
            status = HitStatus.objects.filter(name="On progress").first()
            assigment_creator = Spy.objects.filter(pk=spy.id).first()
            hit = Hit(target_name=target_name, target_location=target_location,
                    description=description, hitman_assigned=hitman_assigned,
                    status=status, assigment_creator=assigment_creator)
            hit.save()

    if spy.is_superuser:
        rol = BOSS
        hit_form.fields['hitman_assigned'].queryset = get_hitmans(spy, rol)
    elif spy.is_staff:
        rol = MANAGER
        hit_form.fields['hitman_assigned'].queryset = get_hitmans(spy, rol)
    context = {
        'hit_form':hit_form
    }

    return render(request, 'hits/create_hit.html', context)


    

@login_required
def hits_view(request):
    spy = request.user
    if spy.is_staff and spy.is_superuser: # Boss
        context = get_context(spy, BOSS)
        return render(request, 'hits/boss_hits_view.html', context)
    elif spy.is_staff and not spy.is_superuser: # manager
        context = get_context(spy, MANAGER)          
        return render(request, 'hits/manager_hits.html', context)
    elif not spy.is_staff and not spy.is_superuser: # hitman
        context = get_context(spy, HITMAN)            
        return render(request, 'hits/hitman_hits.html', context)

@login_required
def hit_detail(request, pk):
    hit = None

    context = {
        'spy_rol':HITMAN,
        'hit':None,
        'assigned_hit':False,
    }
    try:
        hit = Hit.objects.get(pk=pk)
    except:
        return render(request, 'hits/hit_detail.html', context)

    reassign_form = ReassignHitForm(request.POST or None, initial={'hitman':hit.hitman_assigned.pk})
    context['reassign_form']=reassign_form

    if request.method == 'POST':
        try:
            data = request.POST['hit_status']
            if data == '1':
                status = HitStatus.objects.get(name=COMPLETED)
                hit.status = status
                hit.save()
            elif data == '0':
                status = HitStatus.objects.get(name=FAILED)
                hit.status = status
                hit.save()
        except:
            next
        
        if reassign_form.is_valid():
            data_form = reassign_form.cleaned_data
            new_hitman = data_form['hitman']
            hit.hitman_assigned = Spy.objects.get(email=new_hitman)
            hit.save()
            

    spy = request.user

    if spy.is_superuser:
        context['spy_rol'] = BOSS
    elif not spy.is_superuser and spy.is_staff:
        context['spy_rol'] = MANAGER
    
    if hit.hitman_assigned.id == request.user.id:
        context['hit'] = hit
        context['assigned_hit'] = True
        return render(request, 'hits/hit_detail.html', context)
    elif context['spy_rol']==MANAGER or context['spy_rol']==BOSS:
        context['hit'] = hit
        return render(request, 'hits/hit_detail.html', context)

    return render(request, 'hits/hit_detail.html', context)