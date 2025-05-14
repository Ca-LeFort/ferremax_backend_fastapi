# API de Productos para Ferremas 🛍️🔩

¡Bienvenido a la **API de Ferremas**! Esta es una solución backend robusta y eficiente, desarrollada con **FastAPI**, diseñada para la gestión integral de productos en la plataforma de e-commerce Ferremas. Este proyecto forma parte del ramo Integración de Plataformas de DUOC UC.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479a1.svg)](https://www.mysql.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-green.svg)](https://www.uvicorn.org/)
---

## 📖 Índice

- [🌟 Características Destacadas](#características-destacadas)
- [📦 Requisitos Previos](#requisitos-previos)
- [🔧 Instalación y Configuración](#instalación-y-configuración)
  - [1. Clonar el Repositorio](#1-clonar-el-repositorio)
  - [2. Crear y Activar Entorno Virtual](#2-crear-y-activar-entorno-virtual)
  - [3. Instalar Dependencias](#3-instalar-dependencias)
  - [4. Configurar Variables de Entorno](#4-configurar-variables-de-entorno)
  - [5. Configuración de la Base de Datos](#5-configuración-de-la-base-de-datos)
  - [6. Ejecutar el Servidor de Desarrollo](#6-ejecutar-el-servidor-de-desarrollo)
- [ Documentación interactiva](#documentación-interactiva)

---

## Características Destacadas

- **Framework FastAPI**: Aprovecha el rendimiento y la simplicidad de FastAPI.
- **Integración con MySQL**: Diseñada para funcionar sin problemas con una base de datos MySQL.
- **Variables de Entorno**: Personalizable para diferentes entornos de implementación.
- **Autenticación con Claves API**: Endpoints seguros mediante claves API.

---

## Requisitos Previos

Asegúrate de tener instalados los siguientes componentes antes de comenzar:

- Python 3.8 o superior
- Servidor de base de datos MySQL
- Git

---

## Instalación y Configuración

Sigue estos pasos para configurar la API:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Ca-LeFort/ferremax_backend_fastapi
cd ferremax_backend_fastapi
```
### 2. Crear y activar entorno virtual
Se recomienda utilizar un entorno virtual para gestionar las dependencias:

```bash
python -m venv venv
source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
```
### 3. Instalar dependencias

El proyecto utiliza las siguientes bibliotecas de Python:

    FastAPI: Framework web de alto rendimiento para construir APIs.

    Uvicorn: Servidor ASGI ultrarrápido.

    PyMySQL: Cliente MySQL para Python.

    Dotenv: Para gestionar variables de entorno.

Instalalos desde el requirements.txt:
```bash
pip install -r requirements.txt
```
### 4. Configurar variables de entorno
Crea un archivo .env en la raíz del proyecto y agrega las siguientes variables:

```.env
# Configuración de la Base de Datos MySQL
host="localhost"      # Host de MySQL (ej: localhost, una dirección IP, o el nombre del servicio Docker)
user="miusuario"      # Nombre de usuario de MySQL
password="micontraseña"  # Contraseña del usuario de MySQL
db="base_de_datos_ferremas"    # Nombre de la base de datos de MySQL

# Claves API para Autenticación (separadas por comas)
# Genera claves fuertes y únicas. Considera usar un generador de claves.
API_KEYS="clave_secreta_1,otra_clave_segura_2,clave_de_admin_3"
```
Estas variables son esenciales para que la API se conecte a la base de datos MySQL y maneje las solicitudes de forma segura.

### 5. Configuración de la base de datos
Asegúrate de que tu servidor MySQL esté en funcionamiento y de que la base de datos especificada en el archivo .env esté creada. Puedes usar el siguiente comando para crear la base de datos:

```sql
CREATE DATABASE base_de_datos;
```

### 6. Ejecutar el servidor de desarrollo
Con todas las configuraciones en su lugar, inicia el servidor de la API utilizando Uvicorn:
```bash
uvicorn app.main:app --reload
```
El flag `--reload` reiniciará el servidor automáticamente cada vez que detecte cambios en el código, lo cual es muy útil durante el desarrollo.

La API estará disponible en http://127.0.0.1:8000.

---

## Documentación interactiva

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva de la API (Swagger UI) en:

http://127.0.0.1:8000/docs

Aquí podrás explorar todos los endpoints disponibles, ver sus parámetros esperados y probar las solicitudes directamente desde el navegador.

---
