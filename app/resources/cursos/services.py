from app.models import Curso
from app.resources.core import CRUDService


class CursoService(CRUDService[Curso]):
    model = Curso


curso_service = CursoService()
