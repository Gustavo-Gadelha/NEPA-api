import uuid

from app.extensions import db
from app.models.mixins import TimestampMixin, LogMixin


class Edital(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    caminho_arquivo = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), unique=True, nullable=True)

    admin_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('admin.id'), nullable=False)
    admin = db.relationship('Admin', back_populates='editais_criados', foreign_keys='Edital.admin_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
