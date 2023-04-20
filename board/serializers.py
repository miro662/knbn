from rest_framework.serializers import ModelSerializer

from board.models import Board


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ["name", "slug"]
        read_only_fields = ["slug"]
