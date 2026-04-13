from fastapi import FastAPI
from pydantic import BaseModel
from engine import generate_substitutions

app = FastAPI()

valid_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa"]

class RequestBody(BaseModel):
    day: str
    teachers_on_leave: list[str]

@app.get("/")
def root():
    return {"message": "Substitution Engine API is running!"}

@app.post("/generate_substitutions")
def generate(data: RequestBody):
    if data.day not in valid_days:
        return {"error": "Invalid day"}
    
    result = generate_substitutions(data.day, data.teachers_on_leave)
    return {"substitutions": result}
