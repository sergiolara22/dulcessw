from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse  # <- Importar ORJSON
from pydantic import BaseModel
from typing import List

# Usar ORJSON para formatear las respuestas
app = FastAPI(default_response_class=ORJSONResponse)

# Simulando una "base de datos" en memoria
productos = []

# Modelo para los productos
class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    stock: int
    categoria: str


### ✅ RUTAS CRUD ###
@app.get("/")
def home():
    return {"message": "POS Dulcería funcionando 🍬"}

# Leer todos los productos
@app.get("/productos", response_model=List[Producto])
def get_productos():
    return productos

# Crear producto
@app.post("/productos", response_model=Producto)
def create_producto(producto: Producto):
    productos.append(producto)
    return producto

# Actualizar producto
@app.put("/productos/{producto_id}", response_model=Producto)
def update_producto(producto_id: int, nuevo_producto: Producto):
    for index, prod in enumerate(productos):
        if prod.id == producto_id:
            productos[index] = nuevo_producto
            return nuevo_producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Eliminar producto
@app.delete("/productos/{producto_id}")
def delete_producto(producto_id: int):
    for index, prod in enumerate(productos):
        if prod.id == producto_id:
            productos.pop(index)
            return {"message": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")


### ✅ RUTA SIMULACIÓN DE VENTA ###
@app.post("/venta")
def realizar_venta(ids: List[int]):
    total = 0
    for prod_id in ids:
        producto = next((p for p in productos if p.id == prod_id), None)
        if producto:
            total += producto.precio
        else:
            raise HTTPException(status_code=404, detail=f"Producto con ID {prod_id} no encontrado")

    return {"message": "Venta realizada", "total": total}
