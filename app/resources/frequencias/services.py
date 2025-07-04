from app.models import ControleMensal, Presenca, FrequenciaSemanal
from app.resources.core import CRUDService


class ControleMensalService(CRUDService[ControleMensal]):
    model = ControleMensal


controle_mensal_service = ControleMensalService()


class FrequenciaSemanalService(CRUDService[FrequenciaSemanal]):
    model = FrequenciaSemanal


frequencia_semanal_service = FrequenciaSemanalService()


class PresencaService(CRUDService[Presenca]):
    model = Presenca


presenca_service = PresencaService()
