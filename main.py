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
client = MongoClient(os.environ["MONGO_URI"])
# TODO: conectarse al cluster Admonsis  

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

@app.get('/hoteles/{id_hotel}')
def get_hotel_especifico(id_hotel: int):

    hotel = db.hoteles.find_one(
        {"id_hotel": id_hotel},
        {"_id": 0}
    )

    return hotel or {}

@app.get('/resenas_cliente/{documento_cliente}')
def get_resenas_cliente(documento_cliente: int):

    resenas = list(
        db.resenas.find(
            {
                "cliente.documento_cliente": documento_cliente
            },
            {
                "_id": 0
            }
        )
    )

    return resenas

@app.get('/top_hoteles')
def top_hoteles():

    hoteles = list(db.hoteles.find({},{"_id": 0, "nombre_hotel": 1, "calificacion_promedio": 1})
        .sort("calificacion_promedio", -1)
        .limit(10)
    )

    return hoteles

@app.post('hoteles/anadir_hotel')
def anadir_hotel(datos:dict):
    db.hoteles.insert_one(datos)

def actualizar_hotel(id_hotel: int):

    pipeline = [
        {
            "$match": {
                "id_hotel": id_hotel
            }
        },

        {
            "$group": {
                "_id": "$id_hotel",

                "promedio": {
                    "$avg": "$calificacion"
                },

                "cantidad": {
                    "$sum": 1
                }
            }
        }
    ]

    resultado = db.resenas.aggregate(pipeline).to_list(1)

    if resultado:

        promedio = round(resultado[0]["promedio"], 2)
        cantidad = resultado[0]["cantidad"]

        db.hoteles.update_one(
            {"id_hotel": id_hotel},

            {
                "$set": {
                    "calificacion_promedio": promedio,
                    "cantidad_resenas": cantidad
                }
            }
        )


@app.post('resenas/anadir')
def agregar_resena(datos:dict):
    datos["fecha_registro"] = datetime.now.isoformat()
    db.resenas.insert_one(datos)
    actualizar_hotel(datos["id_hotel"])


def actualizar_todos_los_hoteles():

    hoteles = list(db.hoteles.find({}))

    for hotel in hoteles:

        id_hotel = hotel["id_hotel"]

        resenas = list(
            db.resenas.find(
                {"id_hotel": id_hotel}
            )
        )

        cantidad = len(resenas)

        if cantidad == 0:

            db.hoteles.update_one(
                {"id_hotel": id_hotel},
                {
                    "$set": {
                        "calificacion_promedio": 0,
                        "cantidad_resenas": 0
                    }
                }
            )

            continue

        suma = 0

        for r in resenas:
            suma += r["calificacion"]

        promedio = round(suma / cantidad, 2)

        db.hoteles.update_one(
            {"id_hotel": id_hotel},
            {
                "$set": {
                    "calificacion_promedio": promedio,
                    "cantidad_resenas": cantidad
                }
            }
        )

    print("Todos los hoteles fueron actualizados correctamente.")


@app.get('/evolucion_hotel')
def get_evolucion_hotel(id_hotel: int, anio: int):

    resenas_hotel = db.resenas.find({
        "id_hotel": id_hotel
    })

    suma_mes = {}
    cantidad_mes = {}

    for r in resenas_hotel:

        fecha = r["fecha"]

        if fecha.year == anio:

            mes = fecha.month

            if mes not in suma_mes:
                suma_mes[mes] = 0
                cantidad_mes[mes] = 0

            suma_mes[mes] += r["calificacion"]
            cantidad_mes[mes] += 1

    evolucion = []

    for mes in range(1, 13):

        if mes in cantidad_mes:

            promedio = round(
                suma_mes[mes] / cantidad_mes[mes],
                2
            )

        else:
            promedio = 0

        evolucion.append({
            "mes": mes,
            "calificacion_promedio": promedio
        })

    return evolucion

@app.get('/comparacion_ciudad/{ciudad}')
def comparacion_ciudad(ciudad: str):

    hoteles_ciudad = list(
        db.hoteles.find(
            {"ciudad": ciudad},
            {
                "_id": 0,
                "id_hotel": 1,
                "nombre_hotel": 1
            }
        )
    )

    resultado = []

    suma_ciudad = 0
    cantidad_hoteles = 0

    for hotel in hoteles_ciudad:

        id_hotel = hotel["id_hotel"]

        resenas = list(
            db.resenas.find(
                {"id_hotel": id_hotel}
            )
        )

        total = len(resenas)

        if total == 0:
            promedio = 0
            porcentaje_respondidas = 0
            porcentaje_destacadas = 0

        else:

            suma = 0
            respondidas = 0
            destacadas = 0

            for r in resenas:

                suma += r["calificacion"]

                if r.get("respondida") == True:
                    respondidas += 1

                if r["destacada"] == True:
                    destacadas += 1

            promedio = round(suma / total, 2)

            porcentaje_respondidas = round(
                respondidas * 100 / total,
                2
            )

            porcentaje_destacadas = round(
                destacadas * 100 / total,
                2
            )

        resultado.append({
            "hotel": hotel["nombre_hotel"],
            "calificacion_promedio": promedio,
            "total_resenas": total,
            "porcentaje_respondidas": porcentaje_respondidas,
            "porcentaje_destacadas": porcentaje_destacadas
        })

        suma_ciudad += promedio
        cantidad_hoteles += 1

    promedio_ciudad = round(
        suma_ciudad / cantidad_hoteles,
        2
    )

    for r in resultado:

        r["debajo_promedio_ciudad"] = (
            r["calificacion_promedio"] < promedio_ciudad
        )

    return {
        "promedio_ciudad": promedio_ciudad,
        "hoteles": resultado
    }








    
    










