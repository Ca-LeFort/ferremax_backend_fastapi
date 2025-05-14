from fastapi import FastAPI
from app.routers import productos, marcas, tipos_producto
app = FastAPI()
# Incluir los routers
app.include_router(productos.router)
app.include_router(marcas.router)
app.include_router(tipos_producto.router)