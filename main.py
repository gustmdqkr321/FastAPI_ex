from fastapi import FastAPI

app = FastAPI()

@app.get("/add")
async def add_numbers(num1: int, num2: int):
    total = sum(num1,num2)
    return {"result": total}

def sum(a,b):
    return a+b