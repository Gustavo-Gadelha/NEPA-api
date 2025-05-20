from uuid import UUID

from app.extensions import db
from app.models import Projeto
from app.models.enums import StatusProjeto


class ProjetoService:
    def __init__(self, engine=db):
        self._db = engine

    def save(self, projeto: Projeto) -> Projeto:
        self._db.session.add(projeto)
        self._db.session.commit()
        return projeto

    def get_or_404(self, _id: UUID) -> Projeto:
        return self._db.get_or_404(Projeto, _id)

    def get_all(self, *filters) -> list[Projeto]:
        if filters:
            stmt = self._db.select(Projeto).filter(*filters)
        else:
            stmt = self._db.select(Projeto)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        projeto: Projeto = self.get_or_404(_id)
        self._db.session.delete(projeto)
        self._db.session.commit()

    def alterar_status(self, _id: UUID, status: StatusProjeto) -> None:
        projeto: Projeto = self.get_or_404(_id)
        projeto.status = status
        db.session.commit()


projeto_service = ProjetoService()
