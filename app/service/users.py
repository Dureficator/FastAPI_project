from sqlalchemy import select

from app.service.base import BaseService
from app.database import Users, async_session_maker


class UsersService(BaseService):
    model = Users


