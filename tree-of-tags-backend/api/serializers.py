from rest_framework import serializers
from .models import Tree


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "id": instance.id,
            **instance.json,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }

    def to_internal_value(self, data):
        json_data = {
            key: value
            for key, value in data.items()
            if key not in ["id", "created_at", "updated_at"]
        }

        return json_data