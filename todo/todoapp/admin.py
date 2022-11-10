from django.contrib import admin
from todoapp.models import Task, TaskLog

admin.site.register(Task)
admin.site.register(TaskLog)
