from django.contrib import admin
# Models
from .models import (
    Hit,HitStatus,
    TeamManager,
    TeamMembers,
)


admin.site.register(Hit)
admin.site.register(HitStatus)
admin.site.register(TeamManager)
admin.site.register(TeamMembers)