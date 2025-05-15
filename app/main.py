from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import productos, marcas, tipos_producto

app = FastAPI()

#* Configuración de CORS
origins = [
    "https://localhost:4200",
    "https://localhost.localdomain:4200",
    "https://lvh.me:4200",
    "https://vite.lvh.me:4200",
    "https://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  #* Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  #* Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  #* Permitir todos los encabezados
)

# Incluir los routers
app.include_router(productos.router)
app.include_router(marcas.router)
app.include_router(tipos_producto.router)
