from uuid import UUID

from app.models import Professor
from app.resources.core import CRUDService


class ProfessorService(CRUDService[Professor]):
    model = Professor

    def change_activation(self, _id: UUID, ativo: bool) -> None:
        professor = self.get_or_404(_id)
        professor.ativo = ativo
        self._db.session.commit()


professor_service = ProfessorService()
