from datetime import date
from fastapi import APIRouter, Depends

from app.router.hotels import router
from app.database import Users
from app.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked
from app.schemas.bookings import SBooking
from app.service.bookings import BookingService


@router.get('/{hotel_id}/rooms')
async def get_rooms(
        location: str,
        date_from: date,
        date_to: date,
):
    """ Возвращает все номера в отеле"""
    pass
