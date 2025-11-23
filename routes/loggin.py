from fastapi import APIRouter, status
from models.loggin import Login
from models.usuario import User
from controllers.loggin import register_user, login_user

router = APIRouter(prefix="/loggin")

@router.post("/signup")
async def signup(usuario: User):
    return await register_user(usuario)

@router.post("/login")
async def login(usuario: Login):
    return await login_user(usuario)

