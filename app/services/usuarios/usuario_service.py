from uuid import UUID

from app.extensions import db, argon2
from app.models import Usuario


class UsuarioService:
    def __init__(self, engine=db, ph=argon2):
        self._db = engine
        self._ph = ph

    def save(self, usuario: Usuario) -> Usuario:
        self._db.session.add(usuario)
        self._db.session.commit()
        return usuario

    def get_or_404(self, _id: UUID) -> Usuario:
        return self._db.get_or_404(Usuario, _id)

    def get_all(self, *filters) -> list[Usuario]:
        if filters:
            stmt = self._db.select(Usuario).filter(*filters)
        else:
            stmt = self._db.select(Usuario)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        usuario: Usuario = self.get_or_404(_id)
        self._db.session.delete(usuario)
        self._db.session.commit()

    def alterar_ativacao(self, _id: UUID, ativo: bool) -> None:
        usuario = self.get_or_404(_id)
        usuario.ativo = ativo
        self._db.session.commit()

    def alterar_senha(self, _id: UUID, senha: str) -> None:
        usuario: Usuario = self.get_or_404(_id)
        usuario.senha = self._ph.generate_password_hash(senha)
        self._db.session.commit()


usuario_service = UsuarioService()
