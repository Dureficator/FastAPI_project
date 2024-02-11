from datetime import date

from app.router.hotels import router



@router.get('/{hotel_id}/rooms')
async def get_rooms(
        location: str,
        date_from: date,
        date_to: date,
):
    """ Возвращает все номера в отеле"""
    pass

