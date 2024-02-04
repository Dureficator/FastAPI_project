from datetime import date
from fastapi import APIRouter, Depends

from app.database import Users
from app.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked
from app.schemas.bookings import SBooking
from app.service.bookings import BookingService

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingService.find_all(user_id=user.id)


@router.post('')
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
