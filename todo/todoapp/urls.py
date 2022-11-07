from django.urls import path
from todoapp.views import LoginApi, RegistrationApi, TaskApi

urlpatterns = [
    path('login/', LoginApi.as_view(), name='login-api'),
    path('registration/', RegistrationApi.as_view(), name='registration-api'),
    path('task/', TaskApi.as_view(), name='task-api')
]
