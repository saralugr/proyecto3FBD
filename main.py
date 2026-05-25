from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()


@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        response = JSONResponse(content={}, status_code=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


client = MongoClient(os.environ["MONGO_URI"])
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
    hotel = db.hoteles.find_one({"id_hotel": id_hotel}, {"_id": 0})
    return hotel or {}

@app.get('/hotel_por_nombre/{nombre_hotel}')
def hotel_por_nombre(nombre_hotel: str):
    hotel = db.hoteles.find_one({"nombre_hotel": nombre_hotel}, {"_id": 0})
    return hotel or {}



@app.get('/top_hoteles')
def top_hoteles(fecha_inicio: str, fecha_fin: str):
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    except ValueError:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%m/%d/%Y")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha_inicio inválido. Use YYYY-MM-DD o MM/DD/YYYY")

    try:
        fecha_final_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        try:
            fecha_final_dt = datetime.strptime(fecha_fin, "%m/%d/%Y")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha_fin inválido. Use YYYY-MM-DD o MM/DD/YYYY")

    fecha_final_dt = fecha_final_dt.replace(hour=23, minute=59, second=59)

    resenas = list(
        db.resenas.find({
            "fecha": {
                "$gte": fecha_inicio_dt,
                "$lte": fecha_final_dt
            }
        })
    )

    hoteles = {}

    for r in resenas:
        id_hotel = r.get("id_hotel")
        nombre_hotel = r.get("nombre_hotel", f"Hotel {id_hotel}")
        calificacion = r.get("calificacion", 0)

        if id_hotel is None:
            continue

        if id_hotel not in hoteles:
            hoteles[id_hotel] = {
                "nombre_hotel": nombre_hotel,
                "suma": 0,
                "cantidad": 0
            }

        hoteles[id_hotel]["suma"] += calificacion
        hoteles[id_hotel]["cantidad"] += 1

    resultado = []

    for id_hotel in hoteles:
        if hoteles[id_hotel]["cantidad"] == 0:
            continue
            
        promedio = round(hoteles[id_hotel]["suma"] / hoteles[id_hotel]["cantidad"], 2)

        resultado.append({
            "id_hotel": id_hotel,
            "nombre_hotel": hoteles[id_hotel]["nombre_hotel"],
            "calificacion_promedio": promedio
        })

    resultado.sort(key=lambda x: x["calificacion_promedio"], reverse=True)
    return resultado[:10]

@app.post('/hoteles/anadir_hotel')
def anadir_hotel(datos: dict):
    db.hoteles.insert_one(datos)
    return {"mensaje": "Hotel añadido exitosamente"}

def actualizar_hotel(id_hotel: int):
    pipeline = [
        {"$match": {"id_hotel": id_hotel}},
        {"$group": {"_id": "$id_hotel", "promedio": {"$avg": "$calificacion"}, "cantidad": {"$sum": 1}}}
    ]
    resultado = db.resenas.aggregate(pipeline).to_list(1)
    if resultado:
        promedio = round(resultado[0]["promedio"], 2)
        cantidad = resultado[0]["cantidad"]
        db.hoteles.update_one(
            {"id_hotel": id_hotel},
            {"$set": {"calificacion_promedio": promedio, "cantidad_resenas": cantidad}}
        )

@app.post('/resenas/anadir')
def agregar_resena(datos: dict):
    datos["fecha_registro"] = datetime.now().isoformat()
    db.resenas.insert_one(datos)
    actualizar_hotel(datos["id_hotel"])
    return {"mensaje": "Reseña agregada exitosamente"}

def actualizar_todos_los_hoteles():
    hoteles = list(db.hoteles.find({}))
    for hotel in hoteles:
        id_hotel = hotel["id_hotel"]
        resenas = list(db.resenas.find({"id_hotel": id_hotel}))
        cantidad = len(resenas)
        if cantidad == 0:
            db.hoteles.update_one({"id_hotel": id_hotel}, {"$set": {"calificacion_promedio": 0, "cantidad_resenas": 0}})
            continue
        suma = 0
        for r in resenas:
            suma += r["calificacion"]
        promedio = round(suma / cantidad, 2)
        db.hoteles.update_one({"id_hotel": id_hotel}, {"$set": {"calificacion_promedio": promedio, "cantidad_resenas": cantidad}})
    print("Todos los hoteles fueron actualizados correctamente.")

@app.get('/evolucion_hotel')
def get_evolucion_hotel(id_hotel: int, anio: int):
    resenas_hotel = db.resenas.find({"id_hotel": id_hotel})
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
            text = cantidad_mes[mes] + 1
            cantidad_mes[mes] += 1
    evolucion = []
    for mes in range(1, 13):
        if mes in cantidad_mes:
            promedio = round(suma_mes[mes] / cantidad_mes[mes], 2)
        else:
            promedio = 0
        evolucion.append({"mes": mes, "calificacion_promedio": promedio})
    return evolucion

@app.get('/comparacion_ciudad/{ciudad}')
def comparacion_ciudad(ciudad: str):
    hoteles_ciudad = list(db.hoteles.find({"ciudad": ciudad}, {"_id": 0, "id_hotel": 1, "nombre_hotel": 1}))
    resultado = []
    suma_ciudad = 0
    cantidad_hoteles = 0
    for hotel in hoteles_ciudad:
        id_hotel = hotel["id_hotel"]
        resenas = list(db.resenas.find({"id_hotel": id_hotel}))
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
                if r.get("destacada") == True:
                    destacadas += 1
            promedio = round(suma / total, 2)
            porcentaje_respondidas = round(respondidas * 100 / total, 2)
            porcentaje_destacadas = round(destacadas * 100 / total, 2)
        resultado.append({
            "hotel": hotel["nombre_hotel"],
            "calificacion_promedio": promedio,
            "total_resenas": total,
            "porcentaje_respondidas": porcentaje_respondidas,
            "porcentaje_destacadas": porcentaje_destacadas
        })
        suma_ciudad += promedio
        cantidad_hoteles += 1
    if cantidad_hoteles == 0:
        promedio_ciudad = 0
    else:
        promedio_ciudad = round(suma_ciudad / cantidad_hoteles, 2)
    for r in resultado:
        r["debajo_promedio_ciudad"] = (r["calificacion_promedio"] < promedio_ciudad)
    return {"promedio_ciudad": promedio_ciudad, "hoteles": resultado}



@app.post("/resenas/crear")
def crear_resena(datos: dict):
    if not all([datos.get("id_reserva"), datos.get("documento_cliente"), datos.get("id_hotel"), datos.get("calificacion"), datos.get("descripcion")]):
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios")
    if datos.get("calificacion") < 1 or datos.get("calificacion") > 5:
        raise HTTPException(status_code=400, detail="Calificacion debe ser entre 1 y 5")
    if not isinstance(datos.get("descripcion"), str) or len(datos.get("descripcion").strip()) == 0:
        raise HTTPException(status_code=400, detail="La descripcion no puede estar vacia")
    if db.resenas.find_one({"id_reserva": datos.get("id_reserva"), "cliente.documento_cliente": datos.get("documento_cliente")}):
        raise HTTPException(status_code=409, detail="Ya existe una resena para esta reserva")
    ultima = db.resenas.find_one({}, sort=[("id_resena", -1)])
    nuevo_id = str((int(ultima["id_resena"]) + 1) if ultima and "id_resena" in ultima else 1)
    db.resenas.insert_one({
        "id_resena": nuevo_id,
        "id_hotel": datos.get("id_hotel"),
        "nombre_hotel": datos.get("nombre_hotel", ""),
        "id_reserva": int(datos.get("id_reserva")),
        "cliente": {"documento_cliente": datos.get("documento_cliente"), "nombre_cliente": datos.get("nombre_cliente", "")},
        "calificacion": datos.get("calificacion"),
        "descripcion": datos.get("descripcion").strip(),
        "fecha": datetime.now(),
        "estado": "publicada",
        "destacada": False,
        "votos_utilidad": 0,
        "votantes": [],
        "respuesta_admin": {"respondida": False, "texto": ""}
    })
    resultado = list(db.resenas.aggregate([{"$match": {"id_hotel": datos.get("id_hotel"), "estado": "publicada"}}, {"$group": {"_id": "$id_hotel", "promedio": {"$avg": "$calificacion"}, "cantidad": {"$sum": 1}}}]))
    if resultado:
        db.hoteles.update_one({"nombre_hotel": datos.get("nombre_hotel")}, {"$set": {"calificacion_promedio": round(resultado[0]["promedio"], 2), "cantidad_resenas": resultado[0]["cantidad"]}})
    return {"mensaje": "Resena creada exitosamente"}


@app.put("/resenas/editar/{id_resena}")
def editar_resena(id_resena: str, datos: dict):
    resena = db.resenas.find_one({"id_resena": id_resena, "cliente.documento_cliente": datos.get("documento_cliente"), "estado": "publicada"})
    
    if not resena:
        raise HTTPException(status_code=404, detail="Resena no encontrada o no pertenece al cliente")
    if datos.get("calificacion") is not None and (datos.get("calificacion") < 1 or datos.get("calificacion") > 5):
        raise HTTPException(status_code=400, detail="Calificacion debe ser entre 1 y 5")
    if datos.get("descripcion") is not None and len(datos.get("descripcion").strip()) == 0:
        raise HTTPException(status_code=400, detail="La descripcion no puede estar vacia")
    
    campos = {}
    if datos.get("calificacion") is not None:
        campos["calificacion"] = datos.get("calificacion")
    if datos.get("descripcion") is not None:
        campos["descripcion"] = datos.get("descripcion").strip()
    
    db.resenas.update_one({"id_resena": id_resena}, {"$set": campos})
    
    resultado = list(db.resenas.aggregate([{"$match": {"id_hotel": resena["id_hotel"], "estado": "publicada"}}, {"$group": {"_id": "$id_hotel", "promedio": {"$avg": "$calificacion"}, "cantidad": {"$sum": 1}}}]))
    
    if resultado:
        
        db.hoteles.update_one({"id_hotel": resena["id_hotel"]}, {"$set": {"calificacion_promedio": round(resultado[0]["promedio"], 2), "cantidad_resenas": resultado[0]["cantidad"]}}, upsert=True)
    return {"mensaje": "Resena actualizada exitosamente"}


@app.delete("/resenas/eliminar/{id_resena}")
def eliminar_resena(id_resena: str, datos: dict):
    resena = db.resenas.find_one({"id_resena": id_resena, "cliente.documento_cliente": datos.get("documento_cliente"), "estado": "publicada"})
    if not resena:
        raise HTTPException(status_code=404, detail="Resena no encontrada o no pertenece al cliente")
    db.resenas.update_one({"id_resena": id_resena}, {"$set": {"estado": "eliminada"}})
    resultado = list(db.resenas.aggregate([{"$match": {"id_hotel": resena["id_hotel"], "estado": "publicada"}}, {"$group": {"_id": "$id_hotel", "promedio": {"$avg": "$calificacion"}, "cantidad": {"$sum": 1}}}]))
    if resultado:
        db.hoteles.update_one({"id_hotel": resena["id_hotel"]}, {"$set": {"calificacion_promedio": round(resultado[0]["promedio"], 2), "cantidad_resenas": resultado[0]["cantidad"]}}, upsert=True)
    else:
        db.hoteles.update_one({"id_hotel": resena["id_hotel"]}, {"$set": {"calificacion_promedio": 0, "cantidad_resenas": 0}})
    return {"mensaje": "Resena eliminada exitosamente"}


@app.get("/resenas/hotel/{id_hotel}")
def get_resenas_hotel(id_hotel: str, orden: str = Query(default="fecha", enum=["fecha", "utilidad"]), pagina: int = Query(default=1, ge=1), por_pagina: int = Query(default=10, ge=1, le=50)):
    campo = "fecha" if orden == "fecha" else "votos_utilidad"
    resenas = list(db.resenas.find({"id_hotel": id_hotel, "estado": "publicada"}, {"_id": 0}).sort(campo, -1).skip((pagina - 1) * por_pagina).limit(por_pagina))
    for r in resenas:
        if "fecha" in r and hasattr(r["fecha"], "isoformat"):
            r["fecha"] = r["fecha"].isoformat()
    return {"total": db.resenas.count_documents({"id_hotel": id_hotel, "estado": "publicada"}), "pagina": pagina, "resenas": resenas}


@app.post("/resenas/votar/{id_resena}")
def votar_resena(id_resena: str, datos: dict):
    resena = db.resenas.find_one({"id_resena": id_resena, "estado": "publicada"})
    if not resena:
        raise HTTPException(status_code=404, detail="Resena no encontrada")
    if datos.get("documento_cliente") in resena.get("votantes", []):
        raise HTTPException(status_code=409, detail="Ya votaste por esta resena")
    if resena["cliente"]["documento_cliente"] == datos.get("documento_cliente"):
        raise HTTPException(status_code=403, detail="No puedes votar tu propia resena")
    db.resenas.update_one({"id_resena": id_resena}, {"$inc": {"votos_utilidad": 1}, "$push": {"votantes": datos.get("documento_cliente")}})
    return {"mensaje": "Voto registrado exitosamente"}


@app.get("/resenas_cliente/{documento_cliente}")
def get_resenas_cliente(documento_cliente: str, orden: str = Query(default="fecha", enum=["fecha", "hotel"])):
    campo = "fecha" if orden == "fecha" else "id_hotel"
    resenas = list(db.resenas.find({"cliente.documento_cliente": documento_cliente}, {"_id": 0}).sort(campo, -1))
    resultado = []
    for r in resenas:
        fecha = r.get("fecha")
        if fecha and hasattr(fecha, "isoformat"):
            fecha = fecha.isoformat()
        resultado.append({
            "id_resena": r.get("id_resena"),
            "id_hotel": r.get("id_hotel"),
            "nombre_hotel": r.get("nombre_hotel"),
            "calificacion": r.get("calificacion"),
            "descripcion": r.get("descripcion"),
            "fecha": fecha,
            "estado": r.get("estado"),
            "votos_utilidad": r.get("votos_utilidad", 0),
            "tiene_respuesta": r.get("respuesta_admin", {}).get("respondida", False),
            "destacada": r.get("destacada", False)
        })
    return resultado