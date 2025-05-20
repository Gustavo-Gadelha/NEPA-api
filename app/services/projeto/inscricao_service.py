from uuid import UUID

from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models import Inscricao
from app.models.enums import StatusInscricao


class InscricaoService:
    def __init__(self, engine=db):
        self._db = engine

    def save(self, inscricao: Inscricao) -> Inscricao:
        self._db.session.add(inscricao)
        self._db.session.commit()
        return inscricao

    def get_or_404(self, _id: UUID) -> Inscricao:
        return self._db.get_or_404(Inscricao, _id)

    def get_all(self, *filters) -> list[Inscricao]:
        if filters:
            stmt = self._db.select(Inscricao).filter(*filters)
        else:
            stmt = self._db.select(Inscricao)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        inscricao: Inscricao = self.get_or_404(_id)
        self._db.session.delete(inscricao)
        self._db.session.commit()

    def get_with_filters(self, *filters):
        inscricao: Inscricao | None = self._db.one_or_404(self._db.select(Inscricao).filter(*filters))
        if inscricao is None:
            raise NotFound('Inscrição não encontrado')

        return inscricao

    def alterar_status(self, _id: UUID, status: StatusInscricao) -> None:
        inscricao = self.get_or_404(_id)
        inscricao.aprovado = status
        self._db.session.commit()


inscricao_service = InscricaoService()
