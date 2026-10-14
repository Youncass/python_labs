class HotelError(Exception):
    pass


class RoomNotFoundError(HotelError):
    pass


class RoomAlreadyBookedError(HotelError):
    pass


class RoomNotBookedError(HotelError):
    pass


class InvalidRoomDataError(HotelError):
    pass
