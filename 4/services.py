from models import Room
from storage import load_rooms, save_rooms, export_csv
from exceptions import *


class HotelService:
    def __init__(self):
        self._rooms = load_rooms()

    def get_all_rooms(self) -> list:
        return self._rooms

    def find_room(self, room_id: int) -> Room:
        for room in self._rooms:
            if room.room_id == room_id:
                return room
        raise RoomNotFoundError(f"Номер с ID {room_id} не найден")

    def add_room(self, room: Room):
        for r in self._rooms:
            if r.room_id == room.room_id:
                raise ValueError(f"Номер с ID {room.room_id} уже существует")
        self._rooms.append(room)
        self._save()

    def remove_room(self, room_id: int):
        room = self.find_room(room_id)
        if not room.is_free():
            raise RoomAlreadyBookedError("Нельзя удалить занятый номер")
        self._rooms.remove(room)
        self._save()

    def book_room(self, room_id: int, guest_name: str) -> Room:
        room = self.find_room(room_id)
        if not room.is_free():
            raise RoomAlreadyBookedError(
                f"Номер {room_id} уже забронирован гостем {room.guest_name}")
        room.book(guest_name)
        self._save()
        return room

    def release_room(self, room_id: int) -> Room:
        room = self.find_room(room_id)
        if room.is_free():
            raise RoomNotBookedError(f"Номер {room_id} и так свободен")
        room.release()
        self._save()
        return room

    def find_available(self, category: str = None, min_capacity: int = 0) -> list:
        result = [r for r in self._rooms if r.is_free()]
        if category:
            result = [r for r in result if category.lower() in r.category.lower()]
        if min_capacity > 0:
            result = [r for r in result if r.capacity >= min_capacity]
        return result

    def calculate_cost(self, room_id: int, nights: int) -> float:
        room = self.find_room(room_id)
        return room.calculate_cost(nights)

    def _save(self) -> None:
        save_rooms(self._rooms)

    def export_to_csv(self) -> None:
        export_csv(self._rooms)
