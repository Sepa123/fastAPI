from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["users"])

# User

class User(BaseModel):
    id: int
    name: str
    lastname: str
    age: int
    url: str

users_list = [User(id=1,name="Sebastian", lastname="Retamal", age=25, url="ssss"),
              User(id=2,name="Sebastian", lastname="Retamal", age=25, url="ssss"),
              User(id=3,name="Sebastian", lastname="Retamal", age=25, url="ssss")]

@router.get("/users")
async def list_users():
    return users_list

# operación por PATH

@router.get("/users/{id}")
async def user(id:int):
    return search_user(id=id)

# operación por QUERY

@router.get("/user/")
async def user(id:int):
    return search_user(id=id)
    
def search_user(id:int):
    try:
        users = filter(lambda user: user.id == id, users_list)
        return list(users)[0]
    except:
        return {"error":"error con la busqueda de usuario"}


# Agregar Usuario

@router.post("/user",status_code=201, response_model=User)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404,detail="El usuario ya existe")
        # return {"error":"el usuario ya existe"}
    else:
        users_list.append(user)
        return users_list
    
@router.delete("/user/{id}")
async def delete_user(id:int):
    for index,saved_user in enumerate(users_list):
        if saved_user.id == id:
           del users_list[index]

    # retorna lista de usuarios
    return users_list

@router.put("/user")
async def update_user(user:User):
    for index,saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
    # retorna el ususario con sus datos modificados
    return user