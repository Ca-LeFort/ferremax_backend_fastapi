import pymysql
from dotenv import load_dotenv
import os

#* Cargar las variables de entorno desde el archivo .env
load_dotenv()

#* Obtener las variables de entorno con valores por defecto
host = os.getenv('host', "").strip()
user = os.getenv('user', "").strip()
password = os.getenv('password', "").strip()
db = os.getenv('db', "").strip()

#* Conectar a la base de datos
def get_cone():
    try:
        #* Validar que todas las variables necesarias estén definidas y no sean cadenas vacías
        for var_name, var_value in [("host", host), ("user", user), ("password", password), ("db", db)]:
            if not var_value:
                raise ValueError(f"La variable de entorno '{var_name}' no está configurada o está vacía.")
        
        #* Intentar conectarse a la base de datos
        cone = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db,
        )
        return cone

    except pymysql.MySQLError as e:
        raise RuntimeError(f"Error al conectar con la base de datos: {str(e)}")

    except ValueError as ve:
        raise RuntimeError(f"Configuración inválida: {str(ve)}")