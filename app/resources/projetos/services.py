from app.core import CRUDService
from app.models import Projeto


class ProjetoService(CRUDService[Projeto]):
    model = Projeto

    def is_owner(self, projeto_id, usuario_id):
        projeto = self.get_or_404(projeto_id)
        return projeto.professor_id == usuario_id


projeto_service = ProjetoService()
