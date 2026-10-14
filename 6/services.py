import inspect
from models import *
from exceptions import *
from decorators import *
from protocols import Reportable


class TaskService:
    def __init__(self):
        self._users: list[User] = []
        self._projects: list[Project] = []
        self._tasks: list[Task] = []

    @log_call
    def add_user(self, user: User) -> User:
        self._users.append(user)
        return user

    @log_call
    def add_project(self, project: Project) -> Project:
        self._projects.append(project)
        return project

    @log_call
    def add_task(self, task: Task) -> Task:
        self._tasks.append(task)
        return task

    # --- Поиск ---
    def find_user(self, user_id: int) -> User:
        for u in self._users:
            if u.user_id == user_id:
                return u
        raise UserNotFoundError(f"Пользователь #{user_id} не найден")

    def find_project(self, project_id: int) -> Project:
        for p in self._projects:
            if p.project_id == project_id:
                return p
        raise ProjectNotFoundError(f"Проект #{project_id} не найден")

    def find_task(self, task_id: int) -> Task:
        for t in self._tasks:
            if t.task_id == task_id:
                return t
        raise TaskNotFoundError(f"Задача #{task_id} не найдена")

    @log_call
    def assign_task(self, task_id: int, user_id: int) -> Task:
        task = self.find_task(task_id)
        user = self.find_user(user_id)
        task.assignee_id = user.user_id
        print(f"Задача #{task_id} назначена на {user.name}")
        return task

    @measure_time
    def get_overdue_tasks(self) -> list[Task]:
        return [t for t in self._tasks if t.is_overdue()]

    @repeat(1)
    def get_user_workload(self) -> dict[str, int]:
        workload = {u.name: 0 for u in self._users}
        for t in self._tasks:
            if t.assignee_id is None:
                continue
            if t.status in (TaskStatus.NEW, TaskStatus.IN_PROGRESS):
                try:
                    user = self.find_user(t.assignee_id)
                    workload[user.name] = workload.get(user.name, 0) + 1
                except UserNotFoundError:
                    pass
        return workload

    def get_statistics(self) -> dict:
        return {
            "total_tasks": len(self._tasks),
            "by_status": {
                status.value: sum(1 for t in self._tasks if t.status == status)
                for status in TaskStatus
            },
            "overdue": len(self.get_overdue_tasks()),
            "unassigned": sum(1 for t in self._tasks if t.assignee_id is None),
        }

    def inspect_object(self, obj) -> None:
        print(f"\n=== ИНФОРМАЦИЯ ОБ ОБЪЕКТЕ ===")
        # 1. type()
        print(f"Тип: {type(obj).__name__}")
        # 2. isinstance() + issubclass()
        for cls_name, cls in [("Task", Task), ("User", User), ("Project", Project)]:
            if isinstance(obj, cls):
                print(f"isinstance({cls_name}): True")
                print(f"issubclass({cls_name}, Reportable): "
                      f"{isinstance(obj, Reportable)}")  # structural check
        # 3. dir() / hasattr() / getattr()
        attrs = [a for a in dir(obj) if not a.startswith("__") and not callable(getattr(obj, a))]
        methods = [a for a in dir(obj) if not a.startswith("__") and callable(getattr(obj, a))]
        print(f"Атрибуты: {attrs}")
        print(f"Методы: {methods}")
        # 4. hasattr() + getattr()
        if hasattr(obj, "get_report_data"):
            print(f"Отчёт: {getattr(obj, 'get_report_data')()}")
        # 5. inspect.signature()
        if hasattr(obj, "change_status"):
            sig = inspect.signature(obj.change_status)
            print(f"Сигнатура change_status: {sig}")
