from app.models import Presenca, FrequenciaSemanal
from app.resources.core import CRUDService


class FrequenciaSemanalService(CRUDService[FrequenciaSemanal]):
    model = FrequenciaSemanal


frequencia_semanal_service = FrequenciaSemanalService()


class PresencaService(CRUDService[Presenca]):
    model = Presenca


presenca_service = PresencaService()
