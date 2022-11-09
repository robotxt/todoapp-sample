import uuid
import logging
from enum import Enum

from django.contrib.auth.models import User

from todoapp.models import Task, TaskLog

logger = logging.getLogger(__name__)


class EventTypes(Enum):
    CREATE_NEW_TASK = 1
    UPDATE_TASK_LOG = 2


subscribers = dict()


def _log__update_task(task: Task, user: User) -> TaskLog:
    return TaskLog.objects.create(
        uid=str(uuid.uuid4()),
        tag="user_task_update",
        task=task,
        value=f"{user.first_name} updated the tasks {task.uid}")


def _log__create_task(task: Task, user) -> TaskLog:
    return TaskLog.objects.create(
        uid=str(uuid.uuid4()),
        tag="user_task_created",
        task=task,
        value=f"{user.first_name} created the tasks {task.uid}")


def subscribe(event_type: str, fn):
    has_event = subscribers.get(event_type, None)

    if not has_event:
        subscribers[event_type] = []

    subscribers[event_type].append(fn)


class Events:

    def __init__(self):
        subscribe(EventTypes.UPDATE_TASK_LOG.name, _log__update_task)
        subscribe(EventTypes.CREATE_NEW_TASK.name, _log__create_task)

    def run_event(self, event_type: EventTypes, task: Task, user: User):
        if event_type.name not in subscribers:
            return

        for fn in subscribers[event_type.name]:
            fn(task, user)
