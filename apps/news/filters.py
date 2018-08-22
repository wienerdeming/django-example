# Python
import django_filters

# Project
from .models import News


class NewsCrudFilters(django_filters.FilterSet):
    created_date = django_filters.DateFromToRangeFilter()
    published_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = News
        fields = ('author', 'is_active', 'created_date', 'published_date', )


class NewsPublicFilters(django_filters.FilterSet):
    published_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = News
        fields = ('author', 'published_date', )
