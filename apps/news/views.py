# Python
from django_filters.rest_framework import DjangoFilterBackend

# REST framework
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework import permissions

# Project
from apps.gauth.permissions import ActionPermission
from .models import News
from .filters import NewsCrudFilters, NewsPublicFilters
from .serializers import NewsCrudSerializer, NewsPublicSerializer


# News Crud
class NewsCurdViewSet(viewsets.ModelViewSet):
    serializer_class = NewsCrudSerializer
    queryset = News.objects.all()
    permission_classes = (ActionPermission, )
    filter_class = NewsCrudFilters
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter,
    )
    search_fields = ('title', 'content', )
    ordering_fields = (
        'id', 'title', 'is_active', 'author',
        'publish_date', 'created_date',
    )


class NewsPublicView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin):
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = NewsPublicSerializer
    queryset = News.objects.filter(is_active=True)
    filter_class = NewsPublicFilters
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter,
    )
    search_fields = ('title', 'content', )
    ordering_fields = ('publish_date', )
