from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE, SET_NULL

Spy = get_user_model()

"""Hit status Model"""

class HitStatus(models.Model):
    name = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}'

"""Hit Model"""
class Hit(models.Model):
    status = models.ForeignKey(HitStatus, null=True ,on_delete=models.SET_NULL)
    target_name = models.CharField(max_length=150)
    target_location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    hitman_assigned = models.ForeignKey(Spy, null=True ,on_delete=models.SET_NULL)
    assigment_creator = models.ForeignKey(Spy, null=True, related_name='creator', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions =(('can_create_hit','Is able to create a Hit',),)

    def __str__(self) -> str:
        return f'status:{self.status} hitman:{self.hitman_assigned}'

"""Teams"""
class TeamManager(models.Model):
    manager = models.ForeignKey(Spy, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'team id:{self.id} manager:{self.manager}'
    

"""Team members"""
class TeamMembers(models.Model):
    hitman = models.ForeignKey(Spy, on_delete=models.CASCADE)
    team = models.ForeignKey(TeamManager, on_delete=models.CASCADE, related_name='manager_team')

    def __str__(self):
        return f'manager: {self.team.manager} hitman:{self.hitman}'
    



