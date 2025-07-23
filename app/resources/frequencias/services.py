from app.core import CRUDService
from app.models import FrequenciaSemanal, Presenca


class FrequenciaSemanalService(CRUDService[FrequenciaSemanal]):
    model = FrequenciaSemanal


frequencia_semanal_service = FrequenciaSemanalService()


class PresencaService(CRUDService[Presenca]):
    model = Presenca


presenca_service = PresencaService()
