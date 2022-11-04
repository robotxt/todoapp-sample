from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    priority = serializers.BooleanField(required=False)


class QueryTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()
