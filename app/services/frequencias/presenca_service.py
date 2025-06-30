from app.models import Presenca
from app.services import CRUDService


class PresencaService(CRUDService[Presenca]):
    model = Presenca


presenca_service = PresencaService()
