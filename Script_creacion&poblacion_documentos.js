db.createCollection("resenas", {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: [
        'id_resena',
        'id_hotel',
        'nombre_hotel',
        'cliente',
        'calificacion',
        'descripcion',
        'destacada',
        'fecha',
        'respuesta_admin'
      ],
      properties: {
        id_resena: {
          bsonType: 'string'
        },
        id_hotel: {
          bsonType: 'int'
        },
        nombre_hotel: {
          bsonType: 'string'
        },
        cliente: {
          bsonType: 'object',
          required: [
            'documento_cliente',
            'nombre_cliente'
          ],
          properties: {
            documento_cliente: {
           bsonType: ['string', 'int'], 
              description: 'Documento de identidad del cliente'
            },
            nombre_cliente: {
              bsonType: 'string'
            }
          }
        },
        calificacion: {
          bsonType: [
            'double',
            'int'
          ],
          minimum: 1,
          maximum: 5
        },
        descripcion: {
          bsonType: 'string'
        },
        destacada: {
          bsonType: 'bool'
        },
        fecha: {
          bsonType: 'date'
        },
        respuesta_admin: {
          bsonType: 'object',
          required: [
            'respondida',
            'texto'
          ],
          properties: {
            respondida: {
              bsonType: 'bool'
            },
            texto: {
              bsonType: 'string'
            }
          }
        }
      }
    }
  }
});
db.resenas.insertMany([
  {
    "id_resena": "1",
    "id_hotel": NumberInt(1),
    "nombre_hotel": "Hotel1",
    "cliente": {
      "documento_cliente": "1234",
      "nombre_cliente": "Juan"
    },
    "calificacion": 4.5,
    "descripcion": "Chévere",
    "destacada": false,
    "fecha": new Date("2026-05-19T15:02:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "1",
    "id_hotel": NumberInt(1),
    "nombre_hotel": "Hotel 1",
    "cliente": {
      "documento_cliente": "CC1",
      "nombre_cliente": "Nombre1 Apellido1"
    },
    "calificacion": 4.5,
    "descripcion": "Excelente servicio y habitaciones limpias",
    "destacada": true,
    "fecha": new Date("2025-01-10T10:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "2",
    "id_hotel": NumberInt(1),
    "nombre_hotel": "Hotel 1",
    "cliente": {
      "documento_cliente": "CC2",
      "nombre_cliente": "Nombre2 Apellido2"
    },
    "calificacion": 4,
    "descripcion": "Muy buena atención",
    "destacada": false,
    "fecha": new Date("2025-02-12T14:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "3",
    "id_hotel": NumberInt(2),
    "nombre_hotel": "Hotel 2",
    "cliente": {
      "documento_cliente": "CC3",
      "nombre_cliente": "Nombre3 Apellido3"
    },
    "calificacion": 3.5,
    "descripcion": "Buena ubicación",
    "destacada": false,
    "fecha": new Date("2025-01-20T12:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "4",
    "id_hotel": NumberInt(2),
    "nombre_hotel": "Hotel 2",
    "cliente": {
      "documento_cliente": "CC4",
      "nombre_cliente": "Nombre4 Apellido4"
    },
    "calificacion": 5,
    "descripcion": "El mejor hotel del viaje",
    "destacada": true,
    "fecha": new Date("2025-03-01T09:30:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "5",
    "id_hotel": NumberInt(3),
    "nombre_hotel": "Hotel 3",
    "cliente": {
      "documento_cliente": "CC5",
      "nombre_cliente": "Nombre5 Apellido5"
    },
    "calificacion": 2.5,
    "descripcion": "El ruido fue incómodo",
    "destacada": false,
    "fecha": new Date("2025-02-03T16:00:00"),
    "respuesta_admin": {
      "respondida": true,
      "texto": "Lamentamos los inconvenientes y esperamos mejorar su experiencia."
    }
  },
  {
    "id_resena": "6",
    "id_hotel": NumberInt(3),
    "nombre_hotel": "Hotel 3",
    "cliente": {
      "documento_cliente": "CC6",
      "nombre_cliente": "Nombre6 Apellido6"
    },
    "calificacion": 4.2,
    "descripcion": "Desayuno excelente",
    "destacada": false,
    "fecha": new Date("2025-04-10T08:15:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "7",
    "id_hotel": NumberInt(4),
    "nombre_hotel": "Hotel 4",
    "cliente": {
      "documento_cliente": "CC7",
      "nombre_cliente": "Nombre7 Apellido7"
    },
    "calificacion": 4.8,
    "descripcion": "Vista increíble al mar",
    "destacada": true,
    "fecha": new Date("2025-02-15T11:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "8",
    "id_hotel": NumberInt(4),
    "nombre_hotel": "Hotel 4",
    "cliente": {
      "documento_cliente": "CC8",
      "nombre_cliente": "Nombre8 Apellido8"
    },
    "calificacion": 3.9,
    "descripcion": "Todo estuvo bien",
    "destacada": false,
    "fecha": new Date("2025-05-01T13:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "9",
    "id_hotel": NumberInt(5),
    "nombre_hotel": "Hotel 5",
    "cliente": {
      "documento_cliente": "CC9",
      "nombre_cliente": "Nombre9 Apellido9"
    },
    "calificacion": 4.7,
    "descripcion": "Excelente experiencia",
    "destacada": true,
    "fecha": new Date("2025-01-28T17:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "10",
    "id_hotel": NumberInt(5),
    "nombre_hotel": "Hotel 5",
    "cliente": {
      "documento_cliente": "CC10",
      "nombre_cliente": "Nombre10 Apellido10"
    },
    "calificacion": 4.1,
    "descripcion": "Muy cómodo",
    "destacada": false,
    "fecha": new Date("2025-03-18T10:20:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "11",
    "id_hotel": NumberInt(6),
    "nombre_hotel": "Hotel 6",
    "cliente": {
      "documento_cliente": "CC11",
      "nombre_cliente": "Nombre11 Apellido11"
    },
    "calificacion": 3,
    "descripcion": "Aceptable",
    "destacada": false,
    "fecha": new Date("2025-04-11T09:00:00"),
    "respuesta_admin": {
      "respondida": true,
      "texto": "Lamentamos los inconvenientes y esperamos mejorar su experiencia."
    }
  },
  {
    "id_resena": "12",
    "id_hotel": NumberInt(6),
    "nombre_hotel": "Hotel 6",
    "cliente": {
      "documento_cliente": "CC12",
      "nombre_cliente": "Nombre12 Apellido12"
    },
    "calificacion": 4.9,
    "descripcion": "Servicio impecable",
    "destacada": true,
    "fecha": new Date("2025-05-09T15:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "13",
    "id_hotel": NumberInt(7),
    "nombre_hotel": "Hotel 7",
    "cliente": {
      "documento_cliente": "CC13",
      "nombre_cliente": "Nombre13 Apellido13"
    },
    "calificacion": 4.3,
    "descripcion": "Muy tranquilo",
    "destacada": false,
    "fecha": new Date("2025-02-09T12:45:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "14",
    "id_hotel": NumberInt(7),
    "nombre_hotel": "Hotel 7",
    "cliente": {
      "documento_cliente": "CC14",
      "nombre_cliente": "Nombre14 Apellido14"
    },
    "calificacion": 3.6,
    "descripcion": "Buen hotel",
    "destacada": false,
    "fecha": new Date("2025-06-12T18:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "15",
    "id_hotel": NumberInt(8),
    "nombre_hotel": "Hotel 8",
    "cliente": {
      "documento_cliente": "CC15",
      "nombre_cliente": "Nombre15 Apellido15"
    },
    "calificacion": 5,
    "descripcion": "Perfecto para vacaciones",
    "destacada": true,
    "fecha": new Date("2025-03-20T11:10:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "16",
    "id_hotel": NumberInt(8),
    "nombre_hotel": "Hotel 8",
    "cliente": {
      "documento_cliente": "CC16",
      "nombre_cliente": "Nombre16 Apellido16"
    },
    "calificacion": 4.4,
    "descripcion": "Muy recomendado",
    "destacada": false,
    "fecha": new Date("2025-04-22T16:30:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "17",
    "id_hotel": NumberInt(9),
    "nombre_hotel": "Hotel 9",
    "cliente": {
      "documento_cliente": "CC17",
      "nombre_cliente": "Nombre17 Apellido17"
    },
    "calificacion": 2.9,
    "descripcion": "Puede mejorar",
    "destacada": false,
    "fecha": new Date("2025-05-05T14:00:00"),
    "respuesta_admin": {
      "respondida": true,
      "texto": "Lamentamos los inconvenientes y esperamos mejorar su experiencia."
    }
  },
  {
    "id_resena": "18",
    "id_hotel": NumberInt(9),
    "nombre_hotel": "Hotel 9",
    "cliente": {
      "documento_cliente": "CC18",
      "nombre_cliente": "Nombre18 Apellido18"
    },
    "calificacion": 4.6,
    "descripcion": "Muy agradable",
    "destacada": true,
    "fecha": new Date("2025-06-01T10:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "19",
    "id_hotel": NumberInt(10),
    "nombre_hotel": "Hotel 10",
    "cliente": {
      "documento_cliente": "CC19",
      "nombre_cliente": "Nombre19 Apellido19"
    },
    "calificacion": 4,
    "descripcion": "Habitaciones cómodas",
    "destacada": false,
    "fecha": new Date("2025-01-17T12:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  },
  {
    "id_resena": "20",
    "id_hotel": NumberInt(10),
    "nombre_hotel": "Hotel 10",
    "cliente": {
      "documento_cliente": "CC20",
      "nombre_cliente": "Nombre20 Apellido20"
    },
    "calificacion": 3.8,
    "descripcion": "Buena relación calidad precio",
    "destacada": false,
    "fecha": new Date("2025-02-27T09:00:00"),
    "respuesta_admin": {
      "respondida": false,
      "texto": ""
    }
  }
]);



db.createCollection("hoteles", {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: [
        'id_hotel',
        'nombre_hotel',
        'calificacion_promedio',
        'cantidad_resenas',
        'administrador',
        'ciudad' 
      ],
      properties: {
        id_hotel: {
          bsonType: 'int',
          description: 'ID numérico del hotel'
        },
        nombre_hotel: {
          bsonType: 'string',
          description: 'Nombre del hotel'
        },
        calificacion_promedio: {
          bsonType: [
            'double',
            'int'
          ],
          minimum: 0,
          maximum: 5,
          description: 'Promedio de calificaciones'
        },
        cantidad_resenas: {
          bsonType: 'int',
          minimum: 0,
          description: 'Cantidad total de reseñas'
        },
        administrador: {
          bsonType: 'object',
          required: [
            'id_admin',
            'nombre_admin'
          ],
          properties: {
            id_admin: {
              bsonType: 'int',
              description: 'ID del administrador'
            },
            nombre_admin: {
              bsonType: 'string',
              description: 'Nombre del administrador'
            }
          }
        },
        ciudad: {
          bsonType: 'string', 
          description: 'Ciudad de ubicación del hotel'
        }
      }
    }
  }
});
db.hoteles.insertMany([
  {
    "id_hotel": NumberInt(1),
    "nombre_hotel": "Hotel 1",
    "calificacion_promedio": 4.33,
    "cantidad_resenas": NumberInt(3),
    "administrador": {
      "id_admin": NumberInt(1),
      "nombre_admin": "Carlos Pérez"
    },
    "ciudad": "Bogotá"
  },
  {
    "id_hotel": NumberInt(2),
    "nombre_hotel": "Hotel 2",
    "calificacion_promedio": 4.25,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(2),
      "nombre_admin": "Laura Gómez"
    },
    "ciudad": "Medellín"
  },
  {
    "id_hotel": NumberInt(3),
    "nombre_hotel": "Hotel 3",
    "calificacion_promedio": 3.35,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(3),
      "nombre_admin": "Andrés Ruiz"
    },
    "ciudad": "Cali"
  },
  {
    "id_hotel": NumberInt(4),
    "nombre_hotel": "Hotel 4",
    "calificacion_promedio": 4.35,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(1),
      "nombre_admin": "Carlos Pérez"
    },
    "ciudad": "Cartagena"
  },
  {
    "id_hotel": NumberInt(5),
    "nombre_hotel": "Hotel 5",
    "calificacion_promedio": 4.4,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(2),
      "nombre_admin": "Laura Gómez"
    },
    "ciudad": "Barranquilla"
  },
  {
    "id_hotel": NumberInt(6),
    "nombre_hotel": "Hotel 6",
    "calificacion_promedio": 3.95,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(3),
      "nombre_admin": "Andrés Ruiz"
    },
    "ciudad": "Bogotá"
  },
  {
    "id_hotel": NumberInt(7),
    "nombre_hotel": "Hotel 7",
    "calificacion_promedio": 3.95,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(1),
      "nombre_admin": "Carlos Pérez"
    },
    "ciudad": "Medellín"
  },
  {
    "id_hotel": NumberInt(8),
    "nombre_hotel": "Hotel 8",
    "calificacion_promedio": 4.7,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(2),
      "nombre_admin": "Laura Gómez"
    },
    "ciudad": "Cali"
  },
  {
    "id_hotel": NumberInt(9),
    "nombre_hotel": "Hotel 9",
    "calificacion_promedio": 3.75,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(3),
      "nombre_admin": "Andrés Ruiz"
    },
    "ciudad": "Cartagena"
  },
  {
    "id_hotel": NumberInt(10),
    "nombre_hotel": "Hotel 10",
    "calificacion_promedio": 3.9,
    "cantidad_resenas": NumberInt(2),
    "administrador": {
      "id_admin": NumberInt(1),
      "nombre_admin": "Carlos Pérez"
    },
    "ciudad": "Barranquilla"
  },
  {
    "id_hotel": NumberInt(11),
    "nombre_hotel": "Hotel 11",
    "calificacion_promedio": NumberInt(0),
    "cantidad_resenas": NumberInt(0),
    "administrador": {
      "id_admin": NumberInt(2),
      "nombre_admin": "Laura Gómez"
    },
    "ciudad": "Bogotá"
  },
  {
    "id_hotel": NumberInt(12),
    "nombre_hotel": "Hotel 12",
    "calificacion_promedio": NumberInt(0),
    "cantidad_resenas": NumberInt(0),
    "administrador": {
      "id_admin": NumberInt(3),
      "nombre_admin": "Andrés Ruiz"
    },
    "ciudad": "Medellín"
  },
  {
    "id_hotel": NumberInt(13),
    "nombre_hotel": "Hotel 13",
    "calificacion_promedio": NumberInt(0),
    "cantidad_resenas": NumberInt(0),
    "administrador": {
      "id_admin": NumberInt(1),
      "nombre_admin": "Carlos Pérez"
    },
    "ciudad": "Cali"
  },
  {
    "id_hotel": NumberInt(14),
    "nombre_hotel": "Hotel 14",
    "calificacion_promedio": NumberInt(0),
    "cantidad_resenas": NumberInt(0),
    "administrador": {
      "id_admin": NumberInt(2),
      "nombre_admin": "Laura Gómez"
    },
    "ciudad": "Cartagena"
  },
  {
    "id_hotel": NumberInt(15),
    "nombre_hotel": "Hotel 15",
    "calificacion_promedio": NumberInt(0),
    "cantidad_resenas": NumberInt(0),
    "administrador": {
      "id_admin": NumberInt(3),
      "nombre_admin": "Andrés Ruiz"
    },
    "ciudad": "Barranquilla"
  }
]);

