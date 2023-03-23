from fastapi import HTTPException, APIRouter, status
from database.models.user import User
from database.client import db_client
from database.schemas.user import user_schema, users_schema
from bson import ObjectId
#   TODO: agregar status code

router = APIRouter(tags=["usersdb"],prefix="/usersdb")

users_list = []

@router.get("/", response_model=list[User])
async def list_users():
    return users_schema(db_client.users.find())   

# operación por PATH

@router.get("/{id}")
async def user(id:str):
    return search_user("_id", ObjectId(id))

# # operación por QUERY

@router.get("/")
async def user(id:str):
    return search_user("_id", ObjectId(id))
    
def search_user(field:str, key):
    try:
        user = user_schema(db_client.users.find_one({field : key}))
        return User(**user)
    except:
        return {"error":"error con la busqueda de usuario"}


# Agregar Usuario

@router.post("/",status_code=201, response_model=User)
async def create_user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=404,detail="El usuario ya existe")
    
    user_dict = dict(user) 
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id":id}))

    return User(**new_user)
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    # retorna lista de usuarios
    if not found:
        return {"error": "no se ha eliminado el usuario"}
    

@router.put("/", response_model=User,status_code=status.HTTP_202_ACCEPTED)
async def update_user(user:User):
    try:
        user_dict =dict(user)
        del user_dict["id"]
        found = db_client.users.find_one_and_replace({"_id": ObjectId(user.id)},
                                                          user_dict)
    except:
        return {"error": "no se ha podido actualizar"}
    if not found:
        return {"error": "no se ha podido actualizar"}
    
    return search_user("_id", ObjectId(user.id))