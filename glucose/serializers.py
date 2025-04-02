from rest_framework import serializers

from .models import Glucose


class GlucoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glucose
        fields = "__all__"


class GlucoseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glucose
        fields = [
            "user_id",
            "timestamp",
            "record_type",
            "glucose_value_trend",
            "glucose_scan",
        ]
