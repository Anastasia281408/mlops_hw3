import os
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.linear_model import LinearRegression 

# Загрузка модели
try:
    with open("model.pkl", "rb") as f:
        MODEL = pickle.load(f)
except FileNotFoundError:
    MODEL = LinearRegression()
    MODEL.fit(np.array([[1], [2]]), np.array([2, 4]))
    print("Warning: Using a generated dummy Linear Regression model.")

# Схема запроса
class PredictRequest(BaseModel):
    x: list[float]

app = FastAPI()

@app.get("/health")
def health():
    """Эндпоинт для проверки статуса и версии модели."""
    return {
        "status": "ok",
        "version": os.getenv("MODEL_VERSION", "v1.0.0"),
        "model_type": MODEL.__class__.__name__
    }

@app.post("/predict")
def predict(request: PredictRequest):
    """Эндпоинт для выполнения инференса."""
    data = np.array(request.x).reshape(-1, 1) 
    try:
        prediction = MODEL.predict(data).tolist()
    except Exception as e:
        return {"error": str(e), "message": "Prediction failed"}
    
    return {
        "model_version": os.getenv("MODEL_VERSION", "v1.0.0"),
        "input": request.x,
        "prediction": prediction
    }
