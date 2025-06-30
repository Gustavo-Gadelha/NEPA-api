from app.models import FrequenciaSemanal
from app.services import CRUDService


class FrequenciaSemanalService(CRUDService[FrequenciaSemanal]):
    model = FrequenciaSemanal


frequencia_semanal_service = FrequenciaSemanalService()
