from pathlib import Path
from uuid import UUID

from slugify import slugify
from sqlalchemy import func
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound

from app.config import EDITAIS_DIR
from app.core import CRUDService
from app.models import Edital


class EditalService(CRUDService[Edital]):
    model = Edital

    def delete(self, edital: Edital) -> None:
        self._delete_file(edital)
        super().delete(edital)

    def get_by_slug_or_404(self, slug: str) -> Edital:
        stmt = self._db.select(self.model).where(self.model.slug == slug)
        edital = self._db.session.scalar(stmt)
        if edital is None:
            raise NotFound('Edital não encontrado')

        return edital

    def update_file(self, _id: UUID, arquivo: FileStorage, dir: Path = EDITAIS_DIR) -> Edital:
        edital = self.get_or_404(_id)
        if edital.caminho_arquivo is not None:
            self._delete_file(edital)

        nome, ext = self._split_filename(arquivo.filename)
        slug = self._generate_slug(nome)
        caminho_abs = dir / f'{slug}.{ext}'
        arquivo.save(caminho_abs)

        edital.slug = slug
        edital.caminho_arquivo = caminho_abs.relative_to(dir).name
        self._db.session.commit()
        return edital

    def _generate_slug(self, filename: str) -> str:
        slug = slugify(filename)
        stmt = self._db.select(func.count(self.model.id)).where(self.model.slug.like(f'{slug}%'))
        total = self._db.session.scalar(stmt)
        return f'{slug}-{total + 1}' if total > 0 else slug

    def _split_filename(self, filename: str) -> tuple[str, str]:
        name, ext = filename.split('.', 1)
        return name, ext

    def _delete_file(self, edital: Edital, dir: Path = EDITAIS_DIR) -> None:
        if edital.caminho_arquivo is None:
            return

        edital.caminho_abs(dir).unlink(missing_ok=True)
        edital.slug = None
        edital.caminho_arquivo = None
        self._db.session.commit()


edital_service = EditalService()
