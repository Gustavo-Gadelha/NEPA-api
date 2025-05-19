from uuid import UUID

from app import db, argon2
from app.models import Usuario


def get_or_404(_id: UUID) -> Usuario:
    return db.get_or_404(Usuario, _id)


def get_all() -> list[Usuario]:
    return db.session.scalars(db.select(Usuario)).all()


def delete(_id: UUID) -> None:
    usuario: Usuario = get_or_404(_id)
    db.session.delete(usuario)
    db.session.commit()


def activate(_id: UUID) -> None:
    usuario = get_or_404(_id)
    usuario.ativo = True
    db.session.commit()


def deactivate(_id: UUID) -> None:
    usuario = get_or_404(_id)
    usuario.ativo = False
    db.session.commit()


def change_password(_id: UUID, senha: str) -> None:
    usuario: Usuario = get_or_404(_id)
    usuario.senha = argon2.generate_password_hash(senha)
    db.session.commit()
