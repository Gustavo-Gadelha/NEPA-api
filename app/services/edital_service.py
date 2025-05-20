import uuid
from pathlib import Path
from typing import Any
from uuid import UUID

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.extensions import db
from app.config import UPLOADS_DIR, ALLOWED_EDITAIS_EXTENSIONS
from app.models import Edital
from app.schemas import edital_schema


def save(dados: dict[str, Any], file: FileStorage, admin_id: UUID) -> Edital:
    edital: Edital = edital_schema.load(dados, partial=True)
    edital.caminho_arquivo = _save_file(file)
    edital.admin_id = admin_id

    db.session.add(edital)
    db.session.commit()
    return edital


def _save_file(file):
    filename, extension = secure_filename(file.filename).split('.')
    file_path: Path = UPLOADS_DIR / f'{uuid.uuid4().hex}.{extension}'
    file.save(file_path)

    return file_path.relative_to(UPLOADS_DIR)


def get_or_404(_id: UUID) -> Edital:
    return db.get_or_404(Edital, _id)


def get_all() -> list[Edital]:
    return db.session.scalars(db.select(Edital)).all()


def delete(_id: UUID) -> None:
    edital: Edital = get_or_404(_id)
    caminho_arquivo: Path = UPLOADS_DIR / edital.caminho_arquivo
    caminho_arquivo.unlink(missing_ok=True)  # TODO: Deve jogar algum aviso caso ele não encontre o arquivo

    db.session.delete(edital)
    db.session.commit()


def get_by_slug_or_404(slug: str) -> Edital:
    return db.session.scalar(db.select(Edital).where(Edital.slug == slug))


def abs_path_to(_id: UUID) -> Path:
    edital: Edital = get_or_404(_id)
    return UPLOADS_DIR / edital.caminho_arquivo


def abs_path_to_by_slug(slug: str) -> Path:
    edital: Edital = get_by_slug_or_404(slug)
    return UPLOADS_DIR / edital.caminho_arquivo


def extension_is_allowed(filename: str):
    clean_filename = secure_filename(filename)
    return '.' in clean_filename and clean_filename.rsplit('.', 1)[1].lower() in ALLOWED_EDITAIS_EXTENSIONS
