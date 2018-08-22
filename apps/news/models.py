# Django
from django.db import models
from django.conf import settings

# Project
from apps.shared.models import BaseModel


class News(BaseModel):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title
