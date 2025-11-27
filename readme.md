# **TASK: Dockerize the FastAPI application (API with database and prediction)**

## **Task Objective**

Your task is to:

1. Run the FastAPI APIs below (with predict + DB endpoints),
2. Create a **Dockerfile**,
3. Build a Docker image,
4. Run it locally,
5. Push the image to a registry (DockerHub or GitHub Container Registry - GHCR).

---

# **Application code (FASTAPI + DB + ML Prediction)**

`main.py` file:

```python
from fastapi import FastAPI
from db.models import PricePrediction
import asyncio
from utils import predict_price
from sqlalchemy.orm import Session
from db import models
from db.database import SessionLocal
from functools import lru_cache
from fastapi import Depends

def get_db(): 
db = SessionLocal() 
try: 
yield db 
finally: 
db.close()

app = FastAPI(title="Housing API")

# Root
@app.get("/")
defroot(): 
return {"message": "API for apartments in Łódź"}

@app.post("/predict")
async def predict(data: PricePrediction): 
predicted_price = await asyncio.get_event_loop().run_in_executor( 
None, predict_price, data.area_m2, data.rooms, data.floor, data.year_built, data.longitude, data.latitude, data.locality 
) 
return {"predicted_price": predicted_price}

@app.get("/offers/")
@lru_cache(maxsize=32)
def read_offers(db: Session = Depends(get_db)): 
return db.query(models.OfferDB).all()
```


---

# **Project structure (required)**

Make sure your repo looks like this:

```
project/ 
main.py 
db/ 
__init__.py 
models.py 
database.py 
utils.py
requirements.txt
```

> If the participant doesn't have `requirements.txt`, they must create it.

--

# **Required file — `requirements.txt`**

Minimal example:

```
fastapi
uvicorn[standard]
sqlalchemy
pydantic
```
And for ML:

```
joblib
scikit-learn
pandas
numpy
```

---

# **Part 1: Create a Dockerfile**

The participant must create a **Dockerfile**:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# 🛠 **Part 2: Build the Docker image**

In the project directory:

```bash
docker build -t housing-api:latest .

```

---

# ▶**Part 3: Run the image locally**

```bash
docker run -p 8000:8000 housing-api:latest
```

Go to:

```
http://localhost:8000
```

The API should return:

```json
{ "message": "API for apartments in Łódź" }
```

---
# **Part 4: Push the image to the registry**

## OPTION 1: GitHub Container Registry (GHCR)

1. Log in:

```bash
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
```

2. Tagging:

```bash
docker tag housing-api:latest ghcr.io/USERNAME/housing-api:latest
```

3.Push:

```bash
docker push ghcr.io/USERNAME/housing-api:latest
```
---
