from fastapi import APIRouter, HTTPException, Depends
from app.database import get_cone
from app.keys import verify_api_key

router = APIRouter(prefix="/tiposproducto", tags=["TiposProducto"])

@router.get("/")
def get_tiposproducto():
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        

        cursor.execute("SELECT id_tipo_prod, nombre FROM TIPO_PRODUCTO")
        

        tp = [
            {"id_tipo_prod": id_tipo_prod, "nombre": nombre}
            for id_tipo_prod, nombre in cursor
        ]
        
        # Cerrar la conexión
        cursor.close()
        cone.close()
        

        if not tp:
            raise HTTPException(status_code=404, detail="No hay tipos de producto registrados")
        
        return tp

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_tipo_prod}")
def get_tipoproducto_por_id(id_tipo_prod: int):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        

        cursor.execute("SELECT id_tipo_prod, nombre FROM TIPO_PRODUCTO WHERE id_tipo_prod = %s", (id_tipo_prod,))
        
        # Obtener resultado
        result = cursor.fetchone()
        
        # Cerrar la conexión
        cursor.close()
        cone.close()
        

        if result is None:
            raise HTTPException(status_code=404, detail=f"No se encontró un tipo de producto con id {id_tipo_prod}")
        
        # Construir la respuesta
        tp = {"id_tipo_prod": result[0], "nombre": result[1]}
        return tp

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/add")
def add_tipoproducto(nombre: str, _: None = Depends(verify_api_key)):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        

        cursor.execute("INSERT INTO TIPO_PRODUCTO (nombre) VALUES (%s)", (nombre,))
        
        # Confirmar los cambios
        cone.commit()
        
        # Cerrar la conexión
        cursor.close()
        cone.close()
        
        # Responder con un mensaje de éxito
        return {"status_code": 201, "detail": "Tipo de producto agregado correctamente"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al agregar el tipo de producto: {str(ex)}")

@router.put("/update/{id_tipo_prod}")
def update_tipoproducto(id_tipo_prod: int, nombre: str, _: None = Depends(verify_api_key)):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        

        cursor.execute("SELECT COUNT(*) FROM TIPO_PRODUCTO WHERE id_tipo_prod = %s", (id_tipo_prod,))
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            raise HTTPException(status_code=404, detail=f"No se encontró un tipo de producto con id {id_tipo_prod}")
        

        cursor.execute("UPDATE TIPO_PRODUCTO SET nombre = %s WHERE id_tipo_prod = %s", (nombre, id_tipo_prod))
        
        # Confirmar los cambios
        cone.commit()
        
        # Cerrar la conexión
        cursor.close()
        cone.close()
        
        # Responder con un mensaje de éxito
        return {"status_code": 200, "detail": f"Tipo de producto con id {id_tipo_prod} actualizado correctamente"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el tipo de producto: {str(ex)}")

@router.delete("/delete/{id_tipo_prod}")
def delete_tipoproducto(id_tipo_prod: int, _: None = Depends(verify_api_key)):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        

        cursor.execute("SELECT COUNT(*) FROM TIPO_PRODUCTO WHERE id_tipo_prod = %s", (id_tipo_prod,))
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            raise HTTPException(status_code=404, detail=f"No se encontró un tipo de producto con id {id_tipo_prod}")
        

        cursor.execute("DELETE FROM TIPO_PRODUCTO WHERE id_tipo_prod = %s", (id_tipo_prod,))
        
        # Confirmar los cambios
        cone.commit()
        
        # Cerrar la conexión
        cursor.close()
        cone.close()
        
        # Responder con un mensaje de éxito
        return {"status_code": 200, "detail": f"Tipo de producto con id {id_tipo_prod} eliminado correctamente"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el tipo de producto: {str(ex)}")
