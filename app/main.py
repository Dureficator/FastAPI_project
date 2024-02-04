from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel
from dataclasses import dataclass
import uvicorn

from app.router import router_bookings, router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
