from app.service.base import BaseService
from app.database import Hotels


class HotelsService(BaseService):
    model = Hotels

"""
with booked_rooms as (
	select * from bookings b
	where 
	(b.date_from >= '2023-05-10' and b.date_from <= '2023-06-30')
	or
	(b.date_from <= '2023-05-10' and b.date_to <= '2023-05-10')
),
rooms_left as (
	select 
		r.id,
		r.hotel_id,
		r."name",
		r.description,
		r.price,
		r.quantity - count(b.room_id) as quantity_left,
		r.services,
		r.image_id
	from rooms r
	left join booked_rooms b
		on r.id = b.room_id
	group by 	r.id,
		r.hotel_id,
		r."name",
		r.description,
		r.price,
		r.quantity,
		r.services::varchar,
		r.image_id
)
select 
	h.id,
	h.name,
	h.location,
	h.services,
	h.image_id,
	sum(r.quantity_left) as rooms_quantity
from hotels h
left join rooms_left r on r.hotel_id = h.id
group by h.id,
		h.name,
		h.location,
		h.services::varchar,
		h.image_id
having sum(r.quantity_left) > 0
"""