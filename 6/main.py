# Лабораторная 6 | Вариант 24 | Система задач

from datetime import date, timedelta

from models import *
from services import TaskService
from exceptions import TaskSystemError
from context import OperationLogger
from protocols import Reportable
from decorators import require_status


def input_int(message: str, predicate=lambda x: True) -> int:
    while True:
        try:
            value = int(input(message + ": "))
        except ValueError:
            print("! Введите целое число")
            continue
        if not predicate(value):
            print("! Неверное значение")
            continue
        return value


def input_date(message: str):
    while True:
        raw = input(message + " (YYYY-MM-DD, Enter - пропустить): ").strip()
        if not raw:
            return None
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("! Неверный формат даты")


def demo_protocol(obj: Reportable):
    print(f"[PROTOCOL] {obj.get_report_data()}")


@require_status(TaskStatus.IN_PROGRESS)
def _do_work(service, task):
    print(f"[WORK] Задача '{task.title}' в работе. Всё ок.")


def main():
    service = TaskService()

    with OperationLogger("Инициализация демо-данных"):
        service.add_user(User(1, "Алексей Иванов", "teamlead"))
        service.add_user(User(2, "Мария Петрова", "developer"))
        service.add_user(User(3, "Сергей Сидоров", "qa"))

        service.add_project(Project(1, "Внутренний портал", "Разработка портала"))
        service.add_project(Project(2, "Мобильное приложение", "iOS/Android"))

        today = date.today()
        service.add_task(Task(1, "Спроектировать БД", 1,
                              status=TaskStatus.IN_PROGRESS,
                              assignee_id=1,
                              deadline=today + timedelta(days=5),
                              priority=1))
        service.add_task(Task(2, "Написать API", 1,
                              status=TaskStatus.NEW,
                              assignee_id=2,
                              deadline=today - timedelta(days=2),  # просрочена
                              priority=1))
        service.add_task(Task(3, "Тестирование модуля", 1,
                              status=TaskStatus.NEW,
                              deadline=today + timedelta(days=10),
                              priority=3))
        service.add_task(Task(4, "Дизайн главного экрана", 2,
                              status=TaskStatus.DONE,
                              assignee_id=2,
                              priority=2))

    while True:
        print("1. Показать все задачи")
        print("2. Показать пользователей")
        print("3. Показать проекты")
        print("4. Назначить задачу пользователю")
        print("5. Изменить статус задачи")
        print("6. Просроченные задачи")
        print("7. Загрузка пользователей")
        print("8. Статистика")
        print("9. Интроспекция объекта")
        print("10. Демонстрация Protocol")
        print("11. Демонстрация @require_status")
        print("0. Выход")

        choice = input_int("Выберите действие", lambda x: 0 <= x <= 11)

        try:
            match choice:
                case 1:
                    for t in service._tasks:
                        print(t.get_report_data())

                case 2:
                    for u in service._users:
                        print(u.get_report_data())

                case 3:
                    for p in service._projects:
                        print(p.get_report_data())

                case 4:
                    task_id = input_int("ID задачи", lambda x: x > 0)
                    user_id = input_int("ID пользователя", lambda x: x > 0)
                    with OperationLogger(f"Назначение задачи #{task_id}"):
                        service.assign_task(task_id, user_id)

                case 5:
                    task_id = input_int("ID задачи", lambda x: x > 0)
                    print("Доступные статусы:")
                    for i, st in enumerate(TaskStatus, 1):
                        print(f"  {i}. {st.value}")
                    idx = input_int("Номер статуса", lambda x: 1 <= x <= len(TaskStatus))
                    new_status = list(TaskStatus)[idx - 1]
                    task = service.find_task(task_id)
                    with OperationLogger(f"Смена статуса задачи #{task_id}"):
                        task.change_status(new_status)
                    print(f"Статус изменён на: {new_status.value}")

                case 6:
                    overdue = service.get_overdue_tasks()
                    if not overdue:
                        print("Просроченных задач нет.")
                    else:
                        print(f"\nПросроченных задач: {len(overdue)}")
                        for t in overdue:
                            print(f"  {t.get_report_data()}")

                case 7:
                    workload = service.get_user_workload()
                    print("\nЗагрузка пользователей (активные задачи):")
                    for name, count in workload.items():
                        print(f"  {name}: {count}")

                case 8:
                    stats = service.get_statistics()
                    print("\nСтатистика:")
                    print(f"Всего задач: {stats['total_tasks']}")
                    print(f"По статусам:")
                    for status, count in stats["by_status"].items():
                        print(f"  {status}: {count}")
                    print(f"Просрочено: {stats['overdue']}")
                    print(f"Без исполнителя: {stats['unassigned']}")

                case 9:
                    print("Выберите объект для интроспекции:")
                    print("1. Задача #1")
                    print("2. Пользователь #1")
                    print("3. Проект #1")
                    obj_choice = input_int("Выбор", lambda x: 1 <= x <= 3)
                    obj = [service._tasks[0], service._users[0], service._projects[0]][obj_choice - 1]
                    service.inspect_object(obj)

                case 10:
                    print("Объекты, соответствующие Protocol Reportable:")
                    demo_protocol(service._tasks[0])
                    demo_protocol(service._users[0])

                case 11:
                    task_id = input_int("ID задачи", lambda x: x > 0)
                    task = service.find_task(task_id)
                    try:
                        with OperationLogger("Требуется статус IN_PROGRESS"):
                            _do_work(service, task)
                    except ValueError as e:
                        print(f"! {e}")

                case 0:
                    print("Выход.")
                    break

        except TaskSystemError as e:
            print(f"! Ошибка системы: {e}")
        except ValueError as e:
            print(f"! Некорректные данные: {e}")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()
