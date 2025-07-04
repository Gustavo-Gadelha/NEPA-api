from pathlib import Path
from uuid import UUID

from slugify import slugify
from sqlalchemy import func
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound

from app.config import EDITAIS_DIR
from app.models import Edital
from app.resources.core import CRUDService


class EditalService(CRUDService[Edital]):
    model = Edital

    def get_by_slug_or_404(self, slug: str) -> Edital:
        stmt = self._db.select(self.model).where(self.model.slug == slug)
        edital = self._db.scalar(stmt)
        if edital is None:
            raise NotFound('Edital não encontrado')

        return edital

    def generate_slug(self, filename: str) -> str:
        slug = slugify(filename)
        stmt = self._db.select(func.count(self.model.id)).where(self.model.slug.like(f'{slug}%'))
        total = self._db.session.scalar(stmt)
        return f'{slug}-{total + 1}' if total > 0 else slug

    def save_file(self, arquivo: FileStorage, filename: str, path: Path = EDITAIS_DIR) -> str:
        caminho_arquivo = path / filename
        arquivo.save(caminho_arquivo)
        return caminho_arquivo.relative_to(EDITAIS_DIR).name

    def delete_file(self, _id: UUID) -> None:
        edital = self.get_or_404(_id)
        caminho_arquivo = self.get_filepath(edital)
        if caminho_arquivo.exists():
            caminho_arquivo.unlink()

    def get_filepath(self, edital: Edital, path: Path = EDITAIS_DIR) -> Path:
        arquivo = path / edital.caminho_arquivo
        if not arquivo.exists():
            raise NotFound('Arquivo não encontrado')

        return arquivo


edital_service = EditalService()
