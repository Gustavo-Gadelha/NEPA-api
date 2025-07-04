from uuid import UUID

from app.models import Aluno
from app.resources.core import CRUDService


class AlunoService(CRUDService[Aluno]):
    model = Aluno

    def change_activation(self, _id: UUID, ativo: bool) -> None:
        aluno = self.get_or_404(_id)
        aluno.ativo = ativo
        self._db.session.commit()


aluno_service = AlunoService()
