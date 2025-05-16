from fastapi import APIRouter, HTTPException, Depends
from app.database import get_cone
from app.keys import verify_api_key

router = APIRouter(prefix="/marcas", tags=["Marcas"])

@router.get("/")
def get_marcas():
    try:
        #* Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        
        #* Ejecutar consulta para obtener todas las marcas
        cursor.execute("SELECT id_marca, nombre FROM MARCA")
        
        # Recuperar las marcas
        marcas = [
            {"id_marca": id_marca, "nombre": nombre}
            for id_marca, nombre in cursor
        ]
        
        #* Cerrar la conexión
        cursor.close()
        cone.close()
        
        #* Verificar si no se encontraron marcas
        if not marcas:
            raise HTTPException(status_code=404, detail="No hay marcas registradas")
        
        return marcas

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_marca}")
def get_marca_por_id(id_marca: int):
    try:
        #* Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        
        #* Ejecutar consulta para obtener la marca por ID
        cursor.execute("SELECT id_marca, nombre FROM MARCA WHERE id_marca = %s", (id_marca,))
        
        #* Obtener resultado
        result = cursor.fetchone()
        
        #* Cerrar la conexión
        cursor.close()
        cone.close()
        
        #* Verificar si la marca existe
        if result is None:
            raise HTTPException(status_code=404, detail=f"No se encontró una marca con id {id_marca}")
        
        #* Construir la respuesta
        marca = {"id_marca": result[0], "nombre": result[1]}
        return marca

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/add")
def add_marca(nombre: str, _: None = Depends(verify_api_key)):
    try:
        #* Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        
        #* Insertar la nueva marca
        cursor.execute("INSERT INTO MARCA (nombre) VALUES (%s)", (nombre,))
        
        #* Confirmar los cambios
        cone.commit()
        
        #* Cerrar la conexión
        cursor.close()
        cone.close()
        
        #* Responder con un mensaje de éxito
        return {"status_code": 201, "detail": "Marca agregada correctamente"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al agregar la marca: {str(ex)}")

@router.put("/update/{id_marca}")
def update_marca(id_marca: int, nombre: str, _: None = Depends(verify_api_key)):
    try:
        #* Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        
        #* Verificar si la marca existe
        cursor.execute("SELECT COUNT(*) FROM MARCA WHERE id_marca = %s", (id_marca,))
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            raise HTTPException(status_code=404, detail=f"No se encontró una marca con id {id_marca}")
        
        #* Actualizar el nombre de la marca
        cursor.execute("UPDATE MARCA SET nombre = %s WHERE id_marca = %s", (nombre, id_marca))
        
        #* Confirmar los cambios
        cone.commit()
        
        #* Cerrar la conexión
        cursor.close()
        cone.close()
        
        #* Responder con un mensaje de éxito
        return {"status_code": 200, "detail": f"Marca con id {id_marca} actualizada correctamente"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la marca: {str(ex)}")

@router.delete("/delete/{id_marca}")
def delete_marca(id_marca: int, _: None = Depends(verify_api_key)):
    try:
        #* Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        
        #* Verificar si la marca existe
        cursor.execute("SELECT COUNT(*) FROM MARCA WHERE id_marca = %s", (id_marca,))
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            raise HTTPException(status_code=404, detail=f"No se encontró una marca con id {id_marca}")
        
        #* Eliminar la marca
        cursor.execute("DELETE FROM MARCA WHERE id_marca = %s", (id_marca,))
        
        #* Confirmar los cambios
        cone.commit()
        
        #* Cerrar la conexión
        cursor.close()
        cone.close()
        
        #* Responder con un mensaje de éxito
        return {"status_code": 200, "detail": f"Marca con id {id_marca} eliminada correctamente"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la marca: {str(ex)}")
