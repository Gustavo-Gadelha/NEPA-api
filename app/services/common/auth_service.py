from flask_jwt_extended import create_refresh_token, create_access_token

from app.extensions import db, argon2
from app.models import Usuario


class AuthService:
    def __init__(self, engine=db, ph=argon2):
        self._db = engine
        self._ph = ph

    def login(self, schema: dict[str, str]) -> Usuario | None:
        login = schema.get('login')
        senha = schema.get('senha')

        usuario = self.get_or_404(login)
        if self._ph.check_password_hash(usuario.senha, senha):
            return usuario

        return None

    def get_or_404(self, login: str) -> Usuario:
        if '@' in login:
            stmt = self._db.select(Usuario).where(Usuario.email == login)
        else:
            stmt = self._db.select(Usuario).where(Usuario.matricula == login)

        return self._db.session.scalar(stmt)

    def create_tokens(self, usuario: Usuario) -> dict[str, str]:
        access_token = create_access_token(identity=usuario)
        refresh_token = create_refresh_token(identity=usuario)
        return {'access_token': access_token, 'refresh_token': refresh_token}


auth_service = AuthService()
