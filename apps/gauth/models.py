# Django
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.utils.translation import gettext_lazy as _
from apps.shared.models import DEFAULT_PERMISSIONS


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32,
                                 null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        default_permissions = DEFAULT_PERMISSIONS
        ordering = ('-id',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()
