import django_filters
from blog.models import Blog


class BlogFilter(django_filters.FilterSet):
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        for v in values:
            qs = qs.filter(tags=v)
        return qs
