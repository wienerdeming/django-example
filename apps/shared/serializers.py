from django.contrib.contenttypes.models import ContentType
# REST framework
from rest_framework import serializers

# Project
from apps.shared.models import History
from apps.gauth.models import User
from apps.gauth.serializers import UserSerializer


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = (
            'id',
            'name'
        )


class HistorySerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer()
    user = UserSerializer()

    class Meta:
        model = History
        fields = (
            'id',
            'user',
            'content_type',
            'object_id',
            'text',
            'created_date'
        )
