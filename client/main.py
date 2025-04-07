import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from os import path

app= FastAPI()
path=path.abspath(__file__)
path=path.replace("main.py", "templates")#trova il path assoluto dei temolates a priori
templates=Jinja2Templates(directory=path)
SERVICE_SERVER_URL="http://server:8000"

@app.get("/")
def call_root_server(request:Request):
    try:
        response=requests.get(SERVICE_SERVER_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500,
                            detail=f"Errorre nella comunicazione col server: {e}")
    data_response=response.json()
    return templates.TemplateResponse('home.html',{"request": request,'response':{response}})

@app.get("/inventory")
def inventory(request: Request):
    try:
        response=requests.get(f"{SERVICE_SERVER_URL}/inventory")
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
        response=requests.get(f"{SERVICE_SERVER_URL}/item/{item_name}")
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