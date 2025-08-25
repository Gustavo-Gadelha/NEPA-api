import uuid
from pathlib import Path

from app.config import EDITAIS_DIR
from app.extensions import db
from app.models.mixins import LogMixin, TimestampMixin


class Edital(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    caminho_arquivo = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), unique=True, nullable=True)

    admin_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('admin.id'), nullable=False)
    admin = db.relationship('Admin', back_populates='editais_criados', foreign_keys='Edital.admin_id')

    def caminho_abs(self, base_dir: Path = EDITAIS_DIR) -> Path | None:
        if not self.caminho_arquivo:
            return None

        return base_dir / self.caminho_arquivo

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
