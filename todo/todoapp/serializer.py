from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RegistrationSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    priority = serializers.BooleanField(required=False)


class UpdateTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField(required=True)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    priority = serializers.BooleanField(required=False)
    status = serializers.ChoiceField([('pending', 'pending'),
                                      ('completed', 'completed'),
                                      ('finished', 'finished')])


class QueryTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()
