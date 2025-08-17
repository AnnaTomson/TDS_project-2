from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI(title="Data Analyst Agent")

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


class Query(BaseModel):
    task: str
    file: str = None


@app.get("/")
def root():
    return {"message": "Data Analyst Agent is running!"}


@app.post("/query")
def query_agent(query: Query):
    if query.file:
        file_path = os.path.join(DATA_DIR, query.file)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {e}")

        if "summary" in query.task.lower():
            return {"summary": df.describe().to_dict()}

        if "columns" in query.task.lower():
            return {"columns": list(df.columns)}

        return {"message": f"Task '{query.task}' not recognized for CSV."}

    return {"message": f"Task '{query.task}' executed (no file provided)."}
