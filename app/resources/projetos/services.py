from uuid import UUID

from app.core import CRUDService
from app.models import Projeto


class ProjetoService(CRUDService[Projeto]):
    model = Projeto

    def owns_project(self, _id: UUID, professor_id: UUID) -> bool:
        return self.get_or_404(_id).professor_id == professor_id


projeto_service = ProjetoService()
