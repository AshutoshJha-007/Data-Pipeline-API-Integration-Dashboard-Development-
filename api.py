
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
import pandas as pd
import config

app = FastAPI()

# Database Connection
engine = create_engine(config.DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "API is live!"}

@app.get("/data")
def get_data():
    df = pd.read_sql("SELECT * FROM data", engine)
    return df.to_dict(orient="records")
