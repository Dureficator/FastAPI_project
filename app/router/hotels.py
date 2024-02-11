from datetime import date
from fastapi import APIRouter

from app.service.hotels import HotelsService
from app.schemas.hotels import SHotel


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get(
    '/{location}',
    response_model=list[SHotel]
)
async def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
):
    """ Возвращает все отели в которых есть свободные номера в период с date_from по date_to"""
    return await HotelsService.find_all(location, date_from, date_to)
