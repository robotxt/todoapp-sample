import uuid
import logging
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

from todoapp.task import NewTasks, UserUpdateTasks, get_task_by_uid
from django.contrib.auth.models import User
from todoapp.serializer import (LoginSerializer, TaskSerializer,
                                QueryTaskSerializer, UpdateTaskSerializer,
                                RegistrationSerializer)
from todoapp.auth import generate_user_token
from todoapp.events import EventTypes, Event

logger = logging.getLogger(__name__)


class InvalidCredentials(AuthenticationFailed):
    pass


class LoginApi(APIView):
    """ Should have basic authentication for app verfication"""

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


class RegistrationApi(APIView):
    """ Should have basic authentication for app verification"""

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        new_user = User.objects.create_user(  # type: ignore
            username=str(uuid.uuid4()),
            email=data['email'],
            password=data['password'],
            first_name=data['firstname'],
            last_name=data['lastname'])

        logger.info("New user created: %s", new_user.email)

        token = generate_user_token(new_user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class TaskApi(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serializer = QueryTaskSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        task_id = serializer.validated_data.get('task_id')

        try:
            task = get_task_by_uid(task_id)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

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

        Event().run_event(EventTypes.CREATE_NEW_TASK, task, request.user)

        logger.info("New Task is created: %s", task.uid)
        return Response({'task_uid': task.uid}, status=status.HTTP_201_CREATED)

    def put(self, request):
        serializer = UpdateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            task = get_task_by_uid(data['task_id'])
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        t = UserUpdateTasks(task=task, user=request.user)
        title = data.get('title', None)
        description = data.get('description', None)
        priority = data.get('priority', None)
        task_status = data.get('status', None)

        try:
            t.validate_permission()
            t.update_task(title=title,
                          description=description,
                          priority=priority,
                          status=task_status)
        except Exception as e:
            return Response({"errors": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        Event().run_event(EventTypes.UPDATE_TASK_LOG, t.task, request.user)

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

        try:
            task = get_task_by_uid(data['task_id'])
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        t = UserUpdateTasks(task=task, user=request.user)
        t.validate_permission()
        t.update_task(status="DELETE")

        return Response({'msg': 'Successfully Deleted'},
                        status=status.HTTP_200_OK)
