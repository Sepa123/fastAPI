from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   responses={404: {"message": "no encontrado"}},
                   tags=["products"])

products_list =  ["Producto1","Producto2","Producto3","Producto4"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]