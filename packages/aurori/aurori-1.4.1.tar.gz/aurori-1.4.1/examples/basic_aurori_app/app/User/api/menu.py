from fastapi import APIRouter

from aurori.api import UserDep
from aurori.pages import menu_builder
api_router = APIRouter()

# index route
@api_router.get('/menu')
def user_menu(user : UserDep):
    menu = menu_builder.build_menu(user)
    return menu