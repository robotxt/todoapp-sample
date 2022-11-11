import uuid
from abc import ABC
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from django.contrib.auth.models import User

from todoapp.models import Task


def generate_task_uid() -> str:
    return str(uuid.uuid4())


def get_task_by_uid(task_id) -> Task:
    try:
        task = Task.objects.get(uid=task_id)
    except Task.DoesNotExist:
        raise Exception("Task not found")

    return task


class TaskStatus(Enum):
    PENDING = 1
    COMPLETE = 2
    DELETED = 3


@dataclass
class NewTasks:
    user: User
    title: str
    description: Optional[str] = ""
    priority: Optional[bool] = False
    uid: str = field(default_factory=generate_task_uid)

    def create(self) -> Task:
        return Task.objects.create(uid=self.uid,
                                   user=self.user,
                                   title=self.title,
                                   description=self.description,
                                   priority=self.priority,
                                   status=TaskStatus.PENDING.name)


@dataclass
class Tasks(ABC):
    task: Task
    user: User


class UserTasks(Tasks):

    def validate_permission(self) -> bool:
        if self.user.pk == self.task.user.pk:
            self._validated_user_permission = True
            return self._validated_user_permission

        raise AssertionError("User permission not allowed")

    def update_task(self,
                    title=None,
                    description=None,
                    priority=None,
                    status=None) -> Task:
        if not hasattr(self, '_validated_user_permission'):
            msg = 'You must call `.validate_permission()` before accessing `.update_task`.'
            raise AssertionError(msg)

        if title:
            self.task.title = title

        if description:
            self.task.description = description

        if priority:
            self.task.priority = priority

        if status:
            new_status = status.upper()
            if new_status in ['COMPLETED', 'FINISHED']:
                self.task.status = TaskStatus.COMPLETE.name
            elif new_status in ['PENDING']:
                self.task.status = TaskStatus.PENDING.name
            elif new_status in ['DELETED', 'DELETE']:
                self.task.status = TaskStatus.DELETED.name
            else:
                raise ValueError("Invalid task status.")

        self.task.save()
        return self.task
