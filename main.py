import asyncio
from functools import lru_cache

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from db import models
from db.database import SessionLocal, engine
from db.models import PricePrediction
from utils import predict_price

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Housing API")


@app.get("/")
def root():
    return {"message": "API do mieszkań we Łodzi"}


@app.post("/predict")
async def predict(data: PricePrediction):
    predicted_price = await asyncio.get_event_loop().run_in_executor(
        None,
        predict_price,
        data.area_m2,
        data.rooms,
        data.floor,
        data.year_built,
        data.longitude,
        data.latitude,
        data.locality,
    )
    return {"predicted_price": predicted_price}


@app.get("/offers/")
@lru_cache(maxsize=32)
def read_offers(db: Session = Depends(get_db)):
    return db.query(models.OfferDB).all()
