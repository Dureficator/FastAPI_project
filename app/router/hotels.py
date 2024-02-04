from datetime import date
from fastapi import APIRouter, Depends

from app.database import Users
from app.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked
from app.schemas.bookings import SBooking
from app.service.bookings import BookingService

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/{location}')
async def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
):
    """ Возвращает все отели в которых есть свободные номера в период с date_from по date_to"""
    pass
