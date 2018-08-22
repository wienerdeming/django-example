# Python
import django_filters

# Project
from .models import History


class HistoryFilter(django_filters.FilterSet):
    created_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = History
        fields = ('user', 'content_type', 'object_id', 'created_date')
