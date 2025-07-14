from app.models import ControleMensal
from app.resources.core import CRUDService


class ControleMensalService(CRUDService[ControleMensal]):
    model = ControleMensal


controle_mensal_service = ControleMensalService()
