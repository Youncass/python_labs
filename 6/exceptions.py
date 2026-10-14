class TaskSystemError(Exception):
    pass


class TaskNotFoundError(TaskSystemError):
    pass


class UserNotFoundError(TaskSystemError):
    pass


class ProjectNotFoundError(TaskSystemError):
    pass


class InvalidStatusTransitionError(TaskSystemError):
    pass
