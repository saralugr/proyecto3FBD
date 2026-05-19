from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#os.environ #para despliegue. #Descomente cuando ya probó todo local.
#client = MongoClient(os.environ["MONGO_URI"])
# TODO: conectarse al cluster Admonsis  
client = MongoClient("mongodb://ISIS2304C11202610:bavnZqjtowm5@157.253.236.88:8087")

# TODO: conectarse a la base de datos Admonsis  
db = client["ISIS2304C11202610"]

@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


@app.get('/resenas')
def get_resenas():
    resenas = list(db.resenas.find({}, {"_id": 0}))
    return resenas

@app.get('/hoteles')
def get_hoteles():
    hoteles = list(db.hoteles.find({}, {"_id": 0}))
    return hoteles

@app.get('/hoteles/{nombre_hotel}')
def get_hotel_especifico(nombre_hotel: str):
    hotel = list(db.hoteles.find_one({"nombre_hotel": nombre_hotel}, {"_id" : 0}))
    return hotel

@app.get('/resenas/{nombre_cliente}')
def get_resenas_especifico(nombre_cliente: str):
    resenas = list(db.resenas.find({"nombre_cliente": nombre_cliente}, {"_id" : 0}))
    return resenas

@app.get('hoteles/top10')
def get_top_10():
    top10 = list(db.hoteles.find({}.sort({"calificacion_proimedio": -1}))).limit(10)
    return top10

    












