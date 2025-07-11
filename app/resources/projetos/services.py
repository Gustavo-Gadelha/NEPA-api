from app.models import Projeto
from app.resources.core import CRUDService


class ProjetoService(CRUDService[Projeto]):
    model = Projeto

    def is_owner(self, projeto_id, usuario):
        projeto = self.get_or_404(projeto_id)
        return projeto.professor_id == usuario.id


projeto_service = ProjetoService()
