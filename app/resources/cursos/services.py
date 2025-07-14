from app.core import CRUDService
from app.models import Curso


class CursoService(CRUDService[Curso]):
    model = Curso


curso_service = CursoService()
