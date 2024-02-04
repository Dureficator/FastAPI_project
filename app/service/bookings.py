from sqlalchemy import select, and_, or_, func, insert

from app.database.database import engine, async_session_maker
from app.service.base import BaseService
from app.database import Bookings, Rooms


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id,
        room_id,
        date_from,
        date_to,
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms')

            query_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            # print(get_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))
            result_rooms_left = await session.execute(query_rooms_left)
            rooms_left: int = result_rooms_left.scalar()

            if rooms_left > 0:
                query_price = select(Rooms.price).filter_by(id=room_id)
                result_price = await session.execute(query_price)
                price: int = result_price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
