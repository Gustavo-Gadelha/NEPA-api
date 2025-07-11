from uuid import UUID

from app.models import Inscricao, Projeto
from app.resources.core import CRUDService


class InscricaoService(CRUDService[Inscricao]):
    model = Inscricao

    def exists_for(self, projeto_id, usuario_id) -> bool:
        stmt = self._db.select(
            self._db.exists().where(self.model.projeto_id == projeto_id, self.model.usuario_id == usuario_id)
        )
        return self._db.session.scalar(stmt)

    def get_by_project(self, project_id: UUID) -> list[Projeto]:
        stmt = self._db.select(self.model).filter_by(project_id=project_id)
        return self._db.session.scalars(stmt).all()


inscricao_service = InscricaoService()
