from app.models import Inscricao
from app.resources.core import CRUDService


class InscricaoService(CRUDService[Inscricao]):
    model = Inscricao

    def exists_for(self, projeto_id, usuario_id) -> bool:
        stmt = self._db.select(
            self._db.exists().where(self.model.projeto_id == projeto_id, self.model.usuario_id == usuario_id)
        )
        return self._db.session.scalar(stmt)


inscricao_service = InscricaoService()
