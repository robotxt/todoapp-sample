from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    priority = serializers.BooleanField(required=False)


class UpdateTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField(required=True)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    priority = serializers.BooleanField(required=False)
    status = serializers.CharField(required=False)


class QueryTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()