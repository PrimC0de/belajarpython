from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SimpleResponse(BaseModel):
    message: str

@app.get("/", response_model=SimpleResponse)
async def read_root():
    return {"message": "Hello World"}
