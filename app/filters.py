import django_filters
from .models import *

# class AuthorFilter(django_filters.FilterSet):
#     author = django_filters.CharFilter(field_name='author', method='filter_category')

#     def filter_category(self, queryset, name, value):
#         authors = value.split(',')
#         return queryset.filter(author__in=authors)

#     class Meta:
#         model = Question
#         fields = ['author']


class AuthorFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', method='filter_category')

    def filter_category(self, queryset,  value):
        categories = value.split(',')
        return queryset.filter(category__in=categories)

    class Meta:
        model = Question
        fields = ['category',]
