import json
import csv
import os
from models import Room


JSON_FILE = "rooms.json"
CSV_FILE = "rooms.csv"


def load_rooms() -> list:
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            rooms = []
            for item in data:
                try:
                    rooms.append(Room.from_dict(item))
                except (KeyError, ValueError) as e:
                    print(f"! Пропущена некорректная запись в JSON: {e}")
            return rooms
    except json.JSONDecodeError as e:
        print(f"! Ошибка чтения JSON: {e}. Начинаем с пустого списка.")
        return []


def save_rooms(rooms: list):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump([room.to_dict() for room in rooms], f, ensure_ascii=False, indent=4)


def export_csv(rooms: list):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["room_id", "category", "price_per_night", "capacity", "status", "guest_name"])

        for room in rooms:
            writer.writerow([room.room_id, room.category, room.price_per_night, room.capacity, room.status, room.guest_name])