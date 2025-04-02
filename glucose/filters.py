import django_filters

from .models import Glucose


class GlucoseFilter(django_filters.FilterSet):
    start = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    stop = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Glucose
        fields = ["user_id", "start", "stop"]
