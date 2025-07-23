from typing import Any
from uuid import UUID

from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import Schema
from werkzeug.exceptions import BadRequest, NotFound

from app.extensions import argon2, db
from app.models import Usuario


class AuthService:
    def __init__(self, engine=db, ph=argon2):
        self._db = engine
        self._ph = ph

    def save(self, usuario: Usuario) -> Usuario:
        self._db.session.add(usuario)
        self._db.session.commit()
        return usuario

    def first(self, **filters):
        stmt = self._db.select(Usuario).filter_by(**filters).limit(1)
        return self._db.session.scalars(stmt).first()

    def find(self, login: str) -> Usuario | None:
        if '@' in login:
            stmt = self._db.select(Usuario).where(Usuario.email == login)
        else:
            stmt = self._db.select(Usuario).where(Usuario.matricula == login)

        return self._db.session.scalar(stmt)

    def login(self, login: str, senha: str) -> Usuario | None:
        usuario = self.find(login)

        if usuario is None:
            raise NotFound(f"Usuário não encontrado com o login '{login}'")
        if self.check_hash(usuario.senha, senha):
            return usuario

        return None

    def register(self, schema: Schema, dados: dict[Any, str]) -> Usuario:
        usuario = schema.load(dados)
        usuario.senha = auth_service.hash(usuario.senha)
        return self.save(usuario)

    def reset_password(self, _id: UUID, password: str):
        usuario = self._db.get_or_404(Usuario, _id)
        if usuario.tipo == 'admin':
            raise BadRequest('A senha desse usuário não pode ser alterada')

        usuario.senha = self.hash(password)
        self._db.session.commit()

    def hash(self, password: str) -> str:
        return self._ph.generate_password_hash(password=password)

    def check_hash(self, hashed: str, password: str) -> bool:
        return self._ph.check_password_hash(hashed, password)

    def create_tokens(self, usuario: Usuario) -> dict[str, str]:
        access_token = create_access_token(identity=usuario)
        refresh_token = create_refresh_token(identity=usuario)
        return {'access_token': access_token, 'refresh_token': refresh_token}


auth_service = AuthService()
