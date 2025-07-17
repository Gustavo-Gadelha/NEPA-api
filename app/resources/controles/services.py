from uuid import UUID

from app.core import CRUDService
from app.models import ControleMensal


class ControleMensalService(CRUDService[ControleMensal]):
    model = ControleMensal

    def owns_controle(self, _id: UUID, professor_id: UUID) -> bool:
        return self.get_or_404(_id).professor_id == professor_id


controle_mensal_service = ControleMensalService()
