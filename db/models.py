from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from .database import Base


class OfferDB(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    price = Column(Float)


class PricePrediction(BaseModel):
    area_m2: float
    rooms: int
    floor: int
    year_built: int
    longitude: float
    latitude: float
    locality: str
