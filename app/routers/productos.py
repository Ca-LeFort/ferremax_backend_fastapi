from fastapi import APIRouter, HTTPException, Depends
from app.database import get_cone
from app.keys import verify_api_key
from typing import Optional

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/")
def get_productos():
    try:
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_producto, nombre, descripcion, precio, stock, imagen_url, id_marca, id_tipo_prod
            FROM PRODUCTO
        """)
        
        productos = [
            {
                "id_producto": id_producto, 
                "nombre": nombre, 
                "descripcion": descripcion, 
                "precio": precio, 
                "stock": stock, 
                "imagen_url": imagen_url, 
                "id_marca": id_marca, 
                "id_tipo_prod": id_tipo_prod
            }
            for id_producto, nombre, descripcion, precio, stock, imagen_url, id_marca, id_tipo_prod in cursor
        ]
        
        cursor.close()
        cone.close()
        
        if not productos:
            raise HTTPException(status_code=404, detail="No hay productos registrados")
        
        return productos

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_producto}")
def get_producto(id_producto: int):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()
        # Consultar el producto por su ID
        cursor.execute("""
            SELECT id_producto, nombre, descripcion, precio, stock, imagen_url, id_marca, id_tipo_prod
            FROM PRODUCTO
            WHERE id_producto = %s
        """, (id_producto,))
        
        # Obtener el resultado
        producto = cursor.fetchone()
        cursor.close()
        cone.close()
        
        # Validar si el producto existe
        if producto is None:
            raise HTTPException(status_code=404, detail=f"Producto con id {id_producto} no encontrado")
        
        # Construir la respuesta
        id_producto, nombre, descripcion, precio, stock, imagen_url, id_marca, id_tipo_prod = producto
        return {
            "id_producto": id_producto,
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio,
            "stock": stock,
            "imagen_url": imagen_url,
            "id_marca": id_marca,
            "id_tipo_prod": id_tipo_prod
        }

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/add")
def add_producto(
    nombre: str, 
    descripcion: str, 
    precio: int, 
    stock: int, 
    imagen_url: str, 
    id_marca: int, 
    id_tipo_prod: int, 
    _: None = Depends(verify_api_key) # Dependencia que solo valida la API key
    ):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")

        cursor = cone.cursor()
        
        query = """
            INSERT INTO PRODUCTO 
            (nombre, descripcion, precio, stock, imagen_url, id_marca, id_tipo_prod)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (nombre, descripcion, precio, stock, imagen_url, id_marca, id_tipo_prod)
        cursor.execute(query, values)
        
        # Confirmar los cambios en la base de datos
        cone.commit()

        # Cerrar conexión
        cursor.close()
        cone.close()

        # Retorno exitoso
        return {"status_code": 200, "detail": "Se agregó el producto correctamente"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al agregar producto: {str(ex)}")

@router.delete("/delete/{id_producto}")
def delete_producto(id_producto: int, _: None = Depends(verify_api_key)):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
        
        cursor = cone.cursor()

        # Verificar si el producto existe antes de eliminarlo
        cursor.execute("SELECT COUNT(*) FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            raise HTTPException(status_code=404, detail=f"Producto con id {id_producto} no encontrado")
        
        # Eliminar el producto
        cursor.execute("DELETE FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
        cone.commit()

        # Cerrar la conexión
        cursor.close()
        cone.close()

        # Respuesta exitosa
        return {"status_code": 200, "detail": f"Producto con id {id_producto} eliminado correctamente"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el producto: {str(ex)}")

@router.patch("/update/{id_producto}")
def update_producto(
    id_producto: int, 
    nombre: Optional[str] = None, 
    descripcion: Optional[str] = None, 
    precio: Optional[int] = None, 
    stock: Optional[int] = None, 
    imagen_url: Optional[str] = None, 
    id_marca: Optional[int] = None, 
    id_tipo_prod: Optional[int] = None,
    _: None = Depends(verify_api_key)
    ):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")

        cursor = cone.cursor()

        # Verificar si el producto existe
        cursor.execute("SELECT COUNT(*) FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            raise HTTPException(status_code=404, detail=f"Producto con id {id_producto} no encontrado")

        # Construir la consulta de actualización dinámicamente
        fields_to_update = []
        values = []
        if nombre is not None:
            fields_to_update.append("nombre = %s")
            values.append(nombre)
        if descripcion is not None:
            fields_to_update.append("descripcion = %s")
            values.append(descripcion)
        if precio is not None:
            fields_to_update.append("precio = %s")
            values.append(precio)
        if stock is not None:
            fields_to_update.append("stock = %s")
            values.append(stock)
        if imagen_url is not None:
            fields_to_update.append("imagen_url = %s")
            values.append(imagen_url)
        if id_marca is not None:
            fields_to_update.append("id_marca = %s")
            values.append(id_marca)
        if id_tipo_prod is not None:
            fields_to_update.append("id_tipo_prod = %s")
            values.append(id_tipo_prod)

        # Si no hay campos para actualizar
        if not fields_to_update:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

        # Agregar el id_producto al final de los valores
        values.append(id_producto)

        # Ejecutar la consulta de actualización
        query = f"UPDATE PRODUCTO SET {', '.join(fields_to_update)} WHERE id_producto = %s"
        cursor.execute(query, values)
        cone.commit()

        # Cerrar la conexión
        cursor.close()
        cone.close()

        # Respuesta exitosa
        return {"status_code": 200, "detail": f"Producto con id {id_producto} actualizado correctamente"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el producto: {str(ex)}")

@router.put("/updatefull/{id_producto}")
def update_producto_full(
    id_producto: int, 
    nombre: str, 
    descripcion: str, 
    precio: int, 
    stock: int, 
    imagen_url: str, 
    id_marca: int, 
    id_tipo_prod: int,
    _: None = Depends(verify_api_key)
    ):
    try:
        # Conectar a la base de datos
        cone = get_cone()
        if cone is None:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")

        cursor = cone.cursor()

        # Verificar si el producto existe
        cursor.execute("SELECT COUNT(*) FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            raise HTTPException(status_code=404, detail=f"Producto con id {id_producto} no encontrado")

        # Actualizar todos los valores obligatorios
        query = """
            UPDATE PRODUCTO
            SET nombre = %s, descripcion = %s, precio = %s, stock = %s, imagen_url = %s, id_marca = %s, id_tipo_prod = %s
            WHERE id_producto = %s
        """
        cursor.execute(query, (nombre, descripcion, precio, stock, imagen_url, id_marca, id_tipo_prod, id_producto))
        cone.commit()

        # Cerrar la conexión
        cursor.close()
        cone.close()

        # Respuesta exitosa
        return {"status_code": 200, "detail": f"Producto con id {id_producto} actualizado correctamente"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el producto: {str(ex)}")