from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener la cadena de claves API y convertirla en una lista
api_keys_env = os.getenv("API_KEYS")

if api_keys_env is None:
    raise ValueError("La variable de entorno 'API_KEYS' no está definida en el archivo .env")

API_KEYS = api_keys_env.split(",")

# Dependencia para verificar la API key
def verify_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Acceso no autorizado: API key inválida")