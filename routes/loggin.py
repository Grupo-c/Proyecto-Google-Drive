from fastapi import APIRouter, status
from models.loggin import Login
from models.usuario import User
from controllers.loggin import register_user_firebase, login_user_firebase

router = APIRouter(prefix="/loggin")

@router.post("/signup")
async def signup(usuario: User):
    return await register_user_firebase(usuario)

@router.post("/login")
async def login(usuario: Login):
    return await login_user_firebase(usuario)

