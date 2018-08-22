from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

DEFAULT_PERMISSIONS = ('list', 'retrieve', 'create', 'update', 'destroy',
                       'get_history', 'write_history')


class BaseManager(models.Manager):
    def get_queryset(self):
        return QuerySetBase(self.model).filter(is_deleted=False)


class QuerySetBase(models.QuerySet):
    as_manager = BaseManager

    def delete(self):
        self.update(is_deleted=True)


class BaseMeta(object):
    ordering = ('-id',)
    default_permissions = DEFAULT_PERMISSIONS


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta(BaseMeta):
        abstract = True

    objects = QuerySetBase.as_manager()


class History(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50)
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField(blank=True)
    before = JSONField(null=True)
    after = JSONField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta(BaseMeta):
        default_permissions = ('list', 'create', )

    @classmethod
    def write_history(cls, user, instance, text):
        return cls.objects.create(
            user=user, text=text, content_object=instance)
