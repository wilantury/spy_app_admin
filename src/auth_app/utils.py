# Django
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
# Consts
from spy_app.constants import BOSS, MANAGER
#Models
from spy_app.models import Hit

Spy = get_user_model()

def set_permissions(user, rol):
    content_type_hit = ContentType.objects.get_for_model(Hit, for_concrete_model=False)
    content_type_spy = ContentType.objects.get_for_model(Spy, for_concrete_model=False)
    hit_permissions = Permission.objects.filter(content_type=content_type_hit)
    spy_permissions = Permission.objects.filter(content_type=content_type_spy)
    print(spy_permissions)
    if rol==MANAGER or BOSS:
        for permission in hit_permissions:
            user.user_permissions.add(permission)
        for permission in spy_permissions:
            user.user_permissions.add(permission)