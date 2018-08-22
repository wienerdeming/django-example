# Django
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# REST framework
from rest_framework.permissions import BasePermission


class ActionPermission(BasePermission):
    """
    Allows access only to has perm users.
    """
    def perm_non_superuser(self, request, view):
        queryset = view.get_queryset()
        content_type = ContentType.objects.get_for_model(queryset.model)
        codename = '%s_%s' % (view.action, content_type.model, )
        perm_exists = Permission.objects\
            .filter(content_type=content_type)\
            .filter(codename=codename)\
            .exists()

        if perm_exists:
            perm_name = '%s.%s' % (content_type.app_label, codename)
            return request.user.has_perm(perm_name)

        return True

    def has_permission(self, request, view):
        if request.user and not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return self.perm_non_superuser(request, view)
