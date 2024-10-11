from enum import Enum


class TaskField(Enum):
    SERVICE_NAME = "service_name"
    SERVICE_ID = "service_id"
    TASK_ID = "task_id"
    STATE = "state"
    CREATED = "created"
    INPUT = "input"
    RESULT = "result"
    STARTED = "started"
    FINISHED = "finished"
    RESULT_URL = "result_url"
