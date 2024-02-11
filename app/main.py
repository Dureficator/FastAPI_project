from fastapi import FastAPI
import uvicorn

from app.router import router_bookings, router_users, router_hotels, router_rooms

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
