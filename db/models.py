from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class OfferDB(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city: Mapped[str] = mapped_column(index=True)
    price: Mapped[float] = mapped_column()

    def __repr__(self):
        return f"<Offer(city={self.city}, price={self.price})>"


class PricePrediction(BaseModel):
    area_m2: float = Field(..., gt=0, description="Area in square meters")
    rooms: int = Field(..., ge=1, description="Number of rooms")
    floor: int = Field(..., ge=0)
    year_built: int = Field(..., ge=1800, le=2030)
    longitude: float
    latitude: float
    city: str
