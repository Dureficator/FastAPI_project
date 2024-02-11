from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: str
    room_quantity: int
    image_id: int


