from uuid import UUID

from app.core import CRUDService
from app.models import Professor


class ProfessorService(CRUDService[Professor]):
    model = Professor

    def change_activation(self, _id: UUID, ativo: bool) -> None:
        professor = self.get_or_404(_id)
        professor.ativo = ativo
        self._db.session.commit()


professor_service = ProfessorService()
