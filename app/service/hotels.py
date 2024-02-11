from sqlalchemy import select, and_, or_, func, Integer, String
from app.service.base import BaseService
from app.database import Hotels
from app.database.database import async_session_maker
from app.database import Bookings, Rooms


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def find_all(
            cls,
            location,
            date_from,
            date_to
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to <= date_from
                    )
                )
            ).cte()

            room_left = select(
                Rooms.hotel_id,
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('quantity_left')
            ).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).group_by(
                Rooms.quantity, Rooms.hotel_id, booked_rooms.c.room_id
            ).cte()

            available_hotels = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services.cast(String),
                (func.sum(room_left.c.quantity_left)).cast(Integer).label('room_quantity'),
                Hotels.image_id,
            ).join(
                room_left, room_left.c.hotel_id == Hotels.id, isouter=True
            ).where(Hotels.location.contains(location)).group_by(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services.cast(String),
                Hotels.image_id,
            ).having(func.sum(room_left.c.quantity_left).label('rooms_quantity') > 0)

            result = await session.execute(available_hotels)
            return [row for row in result.mappings()]
