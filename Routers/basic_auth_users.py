from fastapi import FastAPI, HTTPException, Depends,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "sebastian": {
        "username": "sebastian",
        "full_name": "Sebastian",
        "email": "sebas@gmail.com",
        "disabled": False,
        "password": "qwerty"
    },
    "sebastian2": {
        "username": "sebastian2",
        "full_name": "Juan",
        "email": "sebas2@gmail.com",
        "disabled": True,
        "password": "123456"
    },
}
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token:str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="credenciales no corresponden",
                            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="usuario inactivo",
                            headers={"WWW-Authenticate": "Bearer"})
    return user

@app.post("/login")
async def login_user(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    print(users_db)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="el usuario no es correcto")
    
    user = search_user_db(form.username)

    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="la contraseña no es correcto")

    return {"access_token": user.username,
            "token_type":"bearer"}

@app.get("/users/me")
async def me (user:User = Depends(current_user)):
    return user