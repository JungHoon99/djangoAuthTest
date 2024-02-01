from rest_framework import serializers, exceptions
from todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'detail', 'user_id', 'when', 'how_long']