# Лабораторная 4 | Вариант 9 | Гостиница

from services import HotelService
from models import Room
from exceptions import *


def input_int(message: str, predicate = lambda x: True) -> int:
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


def input_float(message: str, predicate = lambda x: True) -> float:
    while True:
        try:
            value = float(input(message + ": "))
        except ValueError:
            print("! Введите число")
            continue
        if not predicate(value):
            print("! Неверное значение")
            continue
        return value


def show_rooms(rooms: list):
    if not rooms:
        print("! Нет номеров для отображения.")
        return
    for room in rooms:
        print(room.get_info())


def main():
    service = HotelService()

    if not service.get_all_rooms():
        print("База пуста. Добавляем тестовые номера...")
        service.add_room(Room(101, "Стандарт", 3500, 2))
        service.add_room(Room(102, "Стандарт", 3500, 2))
        service.add_room(Room(201, "Люкс", 8500, 3))
        service.add_room(Room(301, "Президентский", 20000, 4))

    while True:
        print("1. Показать все номера")
        print("2. Добавить номер")
        print("3. Удалить номер")
        print("4. Забронировать номер")
        print("5. Освободить номер")
        print("6. Найти свободные номера")
        print("7. Рассчитать стоимость проживания")
        print("8. Экспорт в CSV")
        print("0. Выход")

        choice = input_int("Выберите действие", lambda x: 0 <= x <= 8)

        try:
            match choice:
                case 1:
                    show_rooms(service.get_all_rooms())

                case 2:
                    room_id = input_int("ID номера", lambda x: x > 0)
                    category = input("Категория: ").strip()
                    price = input_float("Цена за ночь", lambda x: x > 0)
                    capacity = input_int("Количество мест", lambda x: x > 0)
                    service.add_room(Room(room_id, category, price, capacity))
                    print("Номер добавлен.")

                case 3:
                    room_id = input_int("ID номера для удаления", lambda x: x > 0)
                    service.remove_room(room_id)
                    print("Номер удалён.")

                case 4:
                    room_id = input_int("ID номера", lambda x: x > 0)
                    guest = input("Имя гостя: ").strip()
                    service.book_room(room_id, guest)
                    print(f"Номер {room_id} забронирован для {guest}.")

                case 5:
                    room_id = input_int("ID номера", lambda x: x > 0)
                    service.release_room(room_id)
                    print(f"Номер {room_id} освобождён.")

                case 6:
                    category = input("Категория (Enter — пропустить): ").strip() or None
                    min_cap = input_int("Мин. мест (0 — не важно)", lambda x: x >= 0)
                    rooms = service.find_available(category, min_cap)
                    print(f"\nНайдено {len(rooms)} свободных номеров:")
                    show_rooms(rooms)

                case 7:
                    room_id = input_int("ID номера", lambda x: x > 0)
                    nights = input_int("Количество ночей", lambda x: x > 0)
                    cost = service.calculate_cost(room_id, nights)
                    print(f"Стоимость проживания: {cost:.2f} руб.")

                case 8:
                    service.export_to_csv()
                    print("Данные экспортированы в rooms.csv")

                case 0:
                    print("Выход. Данные сохранены.")
                    break

        except HotelError as e:
            print(f"! Ошибка: {e}")
        except ValueError as e:
            print(f"! Некорректные данные: {e}")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()
