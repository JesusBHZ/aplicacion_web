from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from models import Personas  

# Configuración de la URL de la base de datos PostgreSQL
DATABASE_URL = ""

# FastAPI app
app = FastAPI()

# Pydantic model para los datos de Personas
class PersonaCreate(BaseModel):
    nombre: str
    telefono: str

class PersonaResponse(BaseModel):
    id_persona: int
    nombre: str
    telefono: str

# Ruta POST para crear una nueva persona
@app.post("/personas/", response_model=PersonaResponse)
async def crear_persona(persona: PersonaCreate):
    try:
        db_persona = await Personas.create(nombre=persona.nombre, telefono=persona.telefono)
        return PersonaResponse(id_persona=db_persona.id_persona, nombre=db_persona.nombre, telefono=db_persona.telefono)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ruta GET para obtener todas las personas
@app.get("/personas/", response_model=List[PersonaResponse])
async def obtener_personas():
    personas = await Personas.all()
    return [PersonaResponse(id_persona=p.id_persona, nombre=p.nombre, telefono=p.telefono) for p in personas]

@app.on_event("startup")
async def init():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["models"]},  
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()

# Configuración de Tortoise ORM con FastAPI
register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},  
    generate_schemas=False,
    add_exception_handlers=True,
)


# uvicorn app.main:app --reload