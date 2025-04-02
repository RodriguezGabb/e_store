from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates=Jinja2Templates(directory="../templates")

API_BASE_URL="http:/127.0.0.1:8000"

#
@app.get("/inventory")
def inventory(request: Request):
    try:
        response=requests.get(f"{API_BASE_URL}/inventory")
        response.raise_for_status()
        inventory=response.json()
    except requests.RequestException as e:
        inventory = []
        print("Errore nella chiamata del API", e)
    res= templates.TemplateResponse(
        "inventory.html",
        {"request":request,"inventory":inventory}
        )
    return res
@app.get("/item/{item_name}")
def item_info(request: Request, item_name:str):
    try:
        response=requests.get(f"{API_BASE_URL}/item/{item_name}")
        response.raise_for_status()
        item=response.json()
    except requests.RequestException as e:
        item= None
        print("Errore nella chiamata del API", e)
    res= templates.TemplateResponse(
        "item_info.html",
        {"request":request, "item":item}
    )
    return res