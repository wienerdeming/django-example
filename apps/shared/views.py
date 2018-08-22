# Django
from django.contrib.contenttypes.models import ContentType

# REST Framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Project
from .models import History
from .serializers import HistorySerializer
from .filters import HistoryFilter


class HistoryView(object):
    """
    Write history of a model instance.
    """

    @action(methods=['get'], detail=True, url_path='history',
            url_name='history')
    def get_history(self, request, *args, **kwargs):
        instance = self.get_object()
        content_type = ContentType.objects.get_for_model(instance)
        queryset = History.objects \
            .filter(content_type=content_type, object_id=instance.pk) \
            .order_by('-created_date')

        queryset = HistoryFilter(request.GET, queryset=queryset).qs

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HistorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='write-history',
            url_name='write-history')
    def write_history(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        text = self.request.data.get('text')

        history = History.write_history(user, instance, text)
        serializer = HistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
