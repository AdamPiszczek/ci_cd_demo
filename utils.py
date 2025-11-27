import random


def predict_price(area_m2, rooms, floor, year_built, longitude, latitude, locality):
    base_price = 5000 * area_m2
    return base_price + random.randint(-10000, 10000)
