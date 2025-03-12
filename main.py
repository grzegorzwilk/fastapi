from fastapi import FastAPI
import subprocess as sub 
import os
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# items = []

# @app.post("/items/")
# def make_item(item: str):
#     items.append(item)
#     return items
# call lpx
@app.get("/lpx")
def run_lpx():
    lp=os.path.dirname(__file__)
    path=os.path.join(lp,'WIN','LP_XMLConverter.exe')
    out = sub.check_output([path])
    return {"result": out}
@app.get("/help")
def help():
    lp=os.path.dirname(__file__)
    path=os.path.join(lp,'WIN','LP_XMLConverter.exe','help')
    out = sub.check_output([path])
    return {"result": out}
