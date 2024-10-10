from aurori import db
from aurori.users.userbase import UserBase
from sqlalchemy import Column, String

class User(UserBase):
    global_user_id = Column(String(255), default="")
    home_server = Column(String(255), default="")
