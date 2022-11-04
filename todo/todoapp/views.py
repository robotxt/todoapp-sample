import logging
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

from todoapp.task import NewTasks
from django.contrib.auth.models import User
from todoapp.models import Task
from todoapp.serializer import LoginSerializer, TaskSerializer, QueryTaskSerializer
from todoapp.auth import generate_user_token

logger = logging.getLogger(__name__)


class InvalidCredentials(AuthenticationFailed):
    pass


class LoginApi(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid Credentials')

        if not user.check_password(data['password']):
            raise AuthenticationFailed('Invalid Credentials')

        token = generate_user_token(user)

        return Response({
            'token': token[0].key,
        }, status=status.HTTP_200_OK)


class TaskApi(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serializer = QueryTaskSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        task_id = serializer.validated_data.get('task_id')

        task = Task.objects.get(uid=task_id)

        return Response(
            {
                'title': task.title,
                'description': task.description,
                'priority': task.priority
            },
            status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        task = NewTasks(user=request.user,
                        title=data['title'],
                        description=data['description'],
                        priority=data['priority'])

        return Response({'task_uid': task.uid}, status=status.HTTP_200_OK)
