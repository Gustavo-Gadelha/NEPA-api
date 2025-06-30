from app.models import ControleMensal
from app.services import CRUDService


class ControleMensalService(CRUDService[ControleMensal]):
    model = ControleMensal


controle_mensal_service = ControleMensalService()
