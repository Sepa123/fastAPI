from fastapi import FastAPI
from Routers import products, users, jwt_auth,users_db
from fastapi.staticfiles import StaticFiles

## iniciar servicio: uvicorn main:app --reload
## doc http://127.0.0.1:8000/docs
## doc http://127.0.0.1:8000/redoc

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth.router)
app.include_router(users_db.router)
app.mount("/static",StaticFiles(directory="Static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hola Mundo"}

@app.get("/ppt",status_code=233)
async def ppt():
    return { "hi":2232 }

@app.get("/item/{item_id}")
async def read_item(item_id):
    return {"item_id":item_id}
