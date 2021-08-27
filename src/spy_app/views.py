from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
# utils
from .utils import get_context, get_hitmans, get_role
from .constants import FAILED, HITMAN, MANAGER, BOSS, COMPLETED
# Models
from .models import Hit, HitStatus, TeamManager, TeamMembers
# Forms
from .forms import ReassignHitForm, HitForm, TeamForm, TeamMembersForm, DeleteMembersForm

Spy = get_user_model()

@login_required
def create_team(request):
    team_form = TeamForm(request.POST or None)
    context = {
        'team_form':team_form,
        'msn':None,
        'msn_type': "danger"
    }

    if request.method == 'POST':
        if team_form.is_valid():
            data_form = team_form.cleaned_data
            manager_team = data_form.get('team_manager')
            team = TeamManager(manager=manager_team)
            team.save()
            context['msn_type'] = "success"
            context['msn'] = "Team created successfully"

    return render(request, 'team/create_team.html', context)



@login_required
@permission_required('auth_app.can_see_hitmen')
def hitman_detail(request, pk):
    spy = request.user
    context = {
        'hitman':None,
        'members': None,
        'members_form':None,
        'msn':None,
        'msn_type': "danger"
    }
    rol = get_role(spy)

    members_form = TeamMembersForm(request.POST or None)
    delete_members_form = DeleteMembersForm(request.POST or None)
    context['members_form'] = members_form
    context['delete_members_form'] = delete_members_form
    team = None
    hitman = Spy.objects.filter(pk=pk).first()
    if hitman:
        if rol==MANAGER:
            team = TeamManager.objects.filter(manager=spy.id).first()
            if team:
                member = TeamMembers.objects.filter(team=team.id).filter(hitman=hitman.id).first()
                if member:
                    context['hitman'] = hitman

        elif rol==BOSS:
            if get_role(hitman) == MANAGER:
                members = get_hitmans(hitman,MANAGER, inactive=True)
                team = TeamManager.objects.filter(manager=hitman.id).first()
                list_hitmen = members.values_list("id")
                available_hitmen = Spy.objects.filter(is_staff=False).filter(is_superuser=False).exclude(id__in=list_hitmen)
                members_form.fields['hitman'].queryset = available_hitmen
                delete_members_form.fields['hitman_member'].queryset = members
                context['hitman'] = hitman
                context['members'] = members
            else:
                context['hitman'] = hitman

    if request.method == 'POST':
        try:
            data = request.POST['inactive_hitman']
            if data == '1':
                hitman.is_active = False
                hitman.save()
                context['msn_type'] = "success"
                context['msn'] = "Hitman status updated"
        except:
            next
        
        if members_form.is_valid():
            if team:
                data_form = members_form.cleaned_data
                member_team = data_form.get('hitman')
                new_member = TeamMembers(hitman=member_team, team=team)
                new_member.save()
                context['msn_type'] = "success"
                context['msn'] = "Member added successfully"
            else:
                context['msn_type'] = "danger"
                context['msn'] = "Manager has not been assigned to a team"
        
        if delete_members_form.is_valid():
            data_form = delete_members_form.cleaned_data
            member_team = data_form.get('hitman_member')
            hitman = TeamMembers.objects.filter(hitman=member_team.id)
            hitman.delete()
            context['msn_type'] = "success"
            context['msn'] = "Member deleted successfully"
        

    return render(request, 'hitmen/hitman_detail.html', context)

@login_required
@permission_required('auth_app.can_see_hitmen')
def hitmen_list(request):
    spy = request.user
    rol = get_role(spy)
    context = {
        'hitmen':None
    }
    hitmen = None
    if rol == MANAGER:
        hitmen = get_hitmans(spy, rol, inactive=True)
    elif rol == BOSS:
        hitmen = get_hitmans(spy, rol, inactive=False)
    context['hitmen'] = hitmen
    
    return render(request, 'hitmen/hitmen.html', context)

@login_required
@permission_required('spy_app.can_create_hit')
def hit_create(request):
    spy = request.user
    rol = None
    hit_form = HitForm(request.POST or None)
    
    context = {
        'hit_form':hit_form,
        'msn':None,
        'msn_type': "danger"
    }

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
            context['msn_type'] = "success"
            context['msn'] = "Hit created successfully"
        else:
            context['msn_type'] = "danger"
            context['msn'] = "Somthing went wrong, check the fields inputs."

    if spy.is_superuser:
        rol = BOSS
        hit_form.fields['hitman_assigned'].queryset = get_hitmans(spy, rol)
    elif spy.is_staff:
        rol = MANAGER
        hit_form.fields['hitman_assigned'].queryset = get_hitmans(spy, rol)

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