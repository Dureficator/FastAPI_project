from fastapi import APIRouter, Response, Depends

from app.database import Users
from app.dependencies import get_current_user
from app.exceptions import UserAlreadyExistsException, IncorrectEMailOrPasswordException
from app.schemas.users import SUserAuth
from app.service.auth import get_password_hash, authenticate_user, create_access_token
from app.service.users import UsersService

router = APIRouter(
    prefix='/auth',
    tags=['Auth & Пользователи'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add_one(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEMailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')


@router.get('/me')
async def read_users_me(curren_user: Users = Depends(get_current_user)):
    return curren_user
