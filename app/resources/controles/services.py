from app.core import CRUDService
from app.models import ControleMensal


class ControleMensalService(CRUDService[ControleMensal]):
    model = ControleMensal


controle_mensal_service = ControleMensalService()
