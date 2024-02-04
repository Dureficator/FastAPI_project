from app.service.base import BaseService
from app.database import Users


class UsersService(BaseService):
    model = Users
