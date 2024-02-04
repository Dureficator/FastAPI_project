from app.service.base import BaseService
from app.database import Rooms


class RoomsService(BaseService):
    model = Rooms