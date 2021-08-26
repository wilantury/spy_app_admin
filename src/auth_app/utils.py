# Django
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
# Consts
from spy_app.constants import BOSS, MANAGER
#Models
from spy_app.models import Hit


def set_permissions(user, rol):
    content_type = ContentType.objects.get_for_model(Hit, for_concrete_model=False)
    hit_permissions = Permission.objects.filter(content_type=content_type)
    if rol==MANAGER or BOSS:
        for permission in hit_permissions:
            user.user_permissions.add(permission)