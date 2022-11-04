import logging
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

from todoapp.task import NewTasks, Tasks, UserTasks
from django.contrib.auth.models import User
from todoapp.models import Task
from todoapp.serializer import (LoginSerializer, TaskSerializer,
                                QueryTaskSerializer, UpdateTaskSerializer)
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
            'token': token.key,
        }, status=status.HTTP_200_OK)


class TaskApi(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serializer = QueryTaskSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        task_id = serializer.validated_data.get('task_id')
        logger.info("Task id: %s", task_id)
        task = Task.objects.get(uid=task_id)

        return Response(
            {
                'task_id': task.uid,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'status': task.status
            },
            status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        task = NewTasks(user=request.user,
                        title=data['title'],
                        description=data['description'],
                        priority=data['priority']).create()

        return Response({'task_uid': task.uid}, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UpdateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        task = Task.objects.get(uid=data['task_id'])
        t = UserTasks(task=task, user=request.user)

        title = data.get('title', None)
        description = data.get('description', None)
        priority = data.get('priority', None)
        task_status = data.get('status', None)

        if title:
            t.update_title(title=title)

        if description:
            t.update_description(description=description)

        if priority:
            t.update_priority(priority=priority)

        if task_status and task_status.upper() in ['COMPLETED', 'FINISHED']:
            t.status_complete()

        if task_status and task_status.upper() in ['PENDING']:
            t.status_pending()

        return Response(
            {
                'task_id': t.task.uid,
                'title': t.task.title,
                'description': t.task.description,
                'priority': t.task.priority,
                'status': t.task.status
            },
            status=status.HTTP_200_OK)

    def delete(self, request):
        serializer = QueryTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        task = Task.objects.get(uid=data['task_id'])

        t = UserTasks(task=task, user=request.user)
        t.delete()

        return Response({'msg': 'Successfully Deleted'},
                        status=status.HTTP_200_OK)
