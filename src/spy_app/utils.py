#django
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
# Models
from .models import Hit, TeamManager, TeamMembers
from .constants import MANAGER, HITMAN, BOSS

Spy = get_user_model()

def get_role(spy):
    if spy.is_superuser:
        return BOSS
    elif not spy.is_superuser and spy.is_staff:
        return MANAGER
    return HITMAN

def get_hitmans(spy, rol, inactive=False):
        if rol == MANAGER:
            team = TeamManager.objects.filter(manager=spy.id).first()
            if team:
                members = TeamMembers.objects.filter(team=team.id).filter().values_list("hitman")
                if not inactive:
                    query_members = Spy.objects.filter(id__in=members).filter(is_active=True)
                else:
                    query_members = Spy.objects.filter(id__in=members)
                return query_members if members else Spy.objects.none()
            return Spy.objects.none()
        elif rol == BOSS:
            if not inactive:
                return Spy.objects.filter(is_superuser=False).filter(is_active=True)
            return Spy.objects.filter(is_superuser=False)


def _get_members_hits(team_members):
    list_hits = []
    if team_members:
        for member in team_members:
            hits = Hit.objects.filter(hitman_assigned=member.hitman.id)
            list_hits.append({ 
                                'email':member.hitman.email,
                                'hits': hits
                            })
    return list_hits

"""Function that return a context according to role"""
def get_context(spy, rol="HITMAN"):
    
    hitmans_hits = Hit.objects.filter(hitman_assigned=spy.id)
    context = {
        'hits':hitmans_hits,
        'team':None,
        'members_team':None
    }
    if rol == HITMAN:
        return context
    elif rol == MANAGER:
        team = TeamManager.objects.filter(manager=spy.id).first()
        if team:
            context['team'] = team
            team_members = TeamMembers.objects.filter(team=team.id)
            list_hits = _get_members_hits(team_members)
            context['members_team'] = list_hits
        return context
    else:
        managers = Spy.objects.filter(is_staff=True).filter(is_superuser=False)
        if managers:
            list_company_hits = []
            list_hits=[]
            members_hits = None
            for manager in managers:
                manager_hits = Hit.objects.filter(hitman_assigned=manager.id)
                team = TeamManager.objects.filter(manager=manager.id).first()
                team_members = None
                if team:
                    team_members = TeamMembers.objects.filter(team=team.id)
                    members_hits = _get_members_hits(team_members)
                list_company_hits.append(
                    {
                        'manager_hits':{
                                'manager':manager,
                                'hits': manager_hits,
                                'team': team,
                                'team_members':members_hits
                            }
                    }
                )
            context['hits'] = list_company_hits
            return context
        else:
            hits_total = Hit.objects.all()
            context['hits'] = hits_total
            return context
