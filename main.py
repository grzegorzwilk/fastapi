from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

items = []

@app.post("/items/")
def make_item(item: str):
    items.append(item)
    return items
