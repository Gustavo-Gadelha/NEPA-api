from pathlib import Path
from uuid import UUID

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.config import EDITAIS_DIR
from app.extensions import db
from app.models import Edital


class EditalService:
    def __init__(self, engine=db):
        self._db = engine

    def save(self, edital: Edital, arquivo: FileStorage) -> Edital:
        filename = secure_filename(arquivo.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        edital.caminho_arquivo = f'{edital.slug}.{ext}'
        self._db.session.add(edital)
        self._db.session.commit()

        caminho_arquivo: Path = EDITAIS_DIR / edital.caminho_arquivo
        arquivo.save(caminho_arquivo)

        return edital

    def get_or_404(self, _id: UUID) -> Edital:
        return self._db.get_or_404(Edital, _id)

    def get_all(self, *filters) -> list[Edital]:
        if filters:
            stmt = self._db.select(Edital).filter(*filters)
        else:
            stmt = self._db.select(Edital)

        return self._db.session.scalars(stmt).all()

    def delete(self, _id: UUID) -> None:
        edital: Edital = self.get_or_404(_id)
        self._db.session.delete(edital)
        self._db.session.commit()

    def get_by_slug_or_404(self, slug: str) -> Edital:
        return self._db.session.scalar(self._db.select(Edital).where(Edital.slug == slug))

    def abs_path_to(self, _id: UUID) -> Path:
        edital: Edital = self.get_or_404(_id)
        return EDITAIS_DIR / edital.caminho_arquivo

    def abs_path_to_by_slug(self, slug: str) -> Path:
        edital: Edital = self.get_by_slug_or_404(slug)
        return EDITAIS_DIR / edital.caminho_arquivo


edital_service = EditalService()
