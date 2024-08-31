from dataclasses import dataclass
from extensions import db
from flask_login import login_user, logout_user

from infra import Mediator
from models import User


@dataclass
class AuthService:
  mediator: Mediator

  def login(self, username: str, password: str) -> None:
    user = User.query.filter_by(username=username).first()
    if not user:
       raise Exception("User not found")
    if user.password != password:
        raise Exception("Invalid password")
    login_user(user)

  def register(self, username: str, password: str, name: str, password_confirmation:str) -> None:
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise Exception("User already exists")
    if password != password_confirmation:
        raise Exception("Password and confirmation do not match")
    user = User(username=username, password=password, name=name)
    db.session.add(user)
    db.session.commit()

  def logout(self):
     logout_user()
     

