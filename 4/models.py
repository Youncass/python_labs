class Room:
    def __init__(self, room_id: int, category: str, price_per_night: float, capacity: int, status: str = "free", guest_name: str = ""):
        self.room_id = room_id
        self.category = category
        self.price_per_night = price_per_night
        self.capacity = capacity
        self.status = status # free | booked
        self.guest_name = guest_name

    @property
    def room_id(self) -> int:
        return self._room_id

    @room_id.setter
    def room_id(self, value: int):
        if value <= 0:
            raise ValueError("ID номера должен быть > 0")
        self._room_id = value

    @property
    def price_per_night(self) -> float:
        return self._price_per_night

    @price_per_night.setter
    def price_per_night(self, value: float):
        if value <= 0:
            raise ValueError("Стоимость должна быть > 0")
        self._price_per_night = value

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value: int):
        if value <= 0:
            raise ValueError("Количество мест должно быть > 0")
        self._capacity = value

    def is_free(self) -> bool:
        return self.status == "free"

    def book(self, guest_name: str):
        if not self.is_free():
            raise ValueError(f"Номер {self.room_id} уже занят")
        if not guest_name.strip():
            raise ValueError("Имя гостя не может быть пустым")
        self.status = "booked"
        self.guest_name = guest_name

    def release(self):
        if self.is_free():
            raise ValueError(f"Номер {self.room_id} и так свободен")
        self.status = "free"
        self.guest_name = ""

    def calculate_cost(self, nights: int) -> float:
        if nights <= 0:
            raise ValueError("Количество ночей должно быть > 0")
        return self.price_per_night * nights

    def get_info(self) -> str:
        guest_info = f", гость: {self.guest_name}" if self.status == "booked" else ""
        return (f"[{self.room_id}] {self.category} | "
                f"{self.price_per_night:.2f} руб/ночь | "
                f"мест: {self.capacity} | статус: {self.status}{guest_info}")

    def to_dict(self) -> dict:
        return {
            "room_id": self.room_id,
            "category": self.category,
            "price_per_night": self.price_per_night,
            "capacity": self.capacity,
            "status": self.status,
            "guest_name": self.guest_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Room":
        return cls(
            room_id=data["room_id"],
            category=data["category"],
            price_per_night=data["price_per_night"],
            capacity=data["capacity"],
            status=data.get("status", "free"),
            guest_name=data.get("guest_name", ""),
        )
