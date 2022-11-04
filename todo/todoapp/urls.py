from django.urls import path
from todoapp.views import LoginApi, TaskApi

urlpatterns = [
    path('login/', LoginApi.as_view(), name='login-api'),
    path('task/', TaskApi.as_view(), name='task-api')
]
