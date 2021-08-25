from .models import Hit, TeamManager, TeamMembers
from .constants import MANAGER, HITMAN

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
            if team_members:
                list_hits = []
                for member in team_members:
                    hits = Hit.objects.filter(hitman_assigned=member.hitman.id)
                    list_hits.append({ 
                                        'email':member.hitman.email,
                                        'hits': hits
                                    })
                context['members_team'] = list_hits
        return context
