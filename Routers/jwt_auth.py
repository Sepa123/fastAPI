from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

router = APIRouter(prefix="/jwt")

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$.kaLkuFrtzilKLNhc3e.lewapPjrMlVtS6DDUhiirLXPX6gGCDlLu"
    },
    "sebastian2": {
        "username": "sebastian2",
        "full_name": "Juan",
        "email": "sebas2@gmail.com",
        "disabled": True,
        "password": "$2a$12$SDWN2eFXMAEqUQlhlq5r1uVZjVHtDBD3HrCmk35qiPKsJpWnSeDti"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token:str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="credenciales no corresponden",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        if username is None:
            raise exception
        
    except JWTError:
        print("hola")
        raise exception

    return search_user(username.get("sub"))

async def current_user(user:User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="usuario inactivo",
                            headers={"WWW-Authenticate": "Bearer"})
    return user

@router.post("/login")
async def login_user(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    # print(users_db)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="el usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="la contraseña no es correcto")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = {"sub": user.username,
                    "exp": expire}
    
    return {"access_token": jwt.encode(access_token,SECRET_KEY, algorithm=ALGORITHM ),
            "token_type":"bearer"}


@router.get("/users/me")
async def me (user:User = Depends(current_user)):
    print("peeerooo")
    return user
# @router.get("/")
# async def hola():
#     return "hola"