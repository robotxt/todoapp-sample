import uuid
from abc import ABC, abstractmethod
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

    @abstractmethod
    def update_title(self, title: str) -> Task:
        pass

    @abstractmethod
    def update_description(self, description: str) -> Task:
        pass

    @abstractmethod
    def update_priority(self, priority: bool) -> Task:
        pass

    @abstractmethod
    def delete(self) -> Task:
        pass

    @abstractmethod
    def status_complete(self) -> Task:
        pass

    @abstractmethod
    def status_pending(self) -> Task:
        pass


class UserTasks(Tasks):

    def update_title(self, title: str) -> Task:
        self.task.title = title
        self.task.save()

        return self.task

    def update_description(self, description: str) -> Task:
        self.task.description = description
        self.task.save()

        return self.task

    def update_priority(self, priority: bool) -> Task:
        self.task.priority = priority
        self.task.save()

        return self.task

    def delete(self):
        self.task.status = TaskStatus.DELETED.name
        self.task.save()

        return self.task

    def status_complete(self):
        self.task.status = TaskStatus.COMPLETE.name
        self.task.save()

        return self.task

    def status_pending(self):
        self.task.status = TaskStatus.PENDING.name
        self.task.save()

        return self.task
