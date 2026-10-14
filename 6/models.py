from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    NEW = "новая"
    IN_PROGRESS = "выполняется"
    DONE = "завершена"
    CANCELLED = "отменена"


@dataclass
class User:
    user_id: int
    name: str
    role: str = "developer"

    def get_report_data(self) -> str:
        return f"Пользователь #{self.user_id}: {self.name} ({self.role})"


@dataclass
class Project:
    project_id: int
    name: str
    description: str = ""

    def get_report_data(self) -> str:
        return f"Проект #{self.project_id}: {self.name}"


@dataclass
class Task:
    task_id: int
    title: str
    project_id: int
    status: TaskStatus = TaskStatus.NEW
    assignee_id: Optional[int] = None
    deadline: Optional[date] = None
    priority: int = 3  # 1 — высокий, 5 — низкий

    def get_report_data(self) -> str:
        assignee = f"исполнитель #{self.assignee_id}" if self.assignee_id else "не назначен"
        deadline = self.deadline.isoformat() if self.deadline else "нет"
        return (f"Задача #{self.task_id}: '{self.title}' | "
                f"статус: {self.status.value} | "
                f"{assignee} | "
                f"дедлайн: {deadline} | "
                f"приоритет: {self.priority}")

    def is_overdue(self) -> bool:
        if self.deadline is None:
            return False
        if self.status in (TaskStatus.DONE, TaskStatus.CANCELLED):
            return False
        return date.today() > self.deadline

    def change_status(self, new_status: TaskStatus) -> None:
        if self.status == new_status:
            return
        
        # Простая проверка переходов
        forbidden = {
            TaskStatus.DONE: {TaskStatus.NEW, TaskStatus.IN_PROGRESS},
            TaskStatus.CANCELLED: {TaskStatus.DONE},
        }
        if new_status in forbidden.get(self.status, set()):
            from exceptions import InvalidStatusTransitionError
            raise InvalidStatusTransitionError(
                f"Нельзя перейти из {self.status.value} в {new_status.value}"
            )
        self.status = new_status
