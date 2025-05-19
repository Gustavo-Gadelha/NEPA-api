import uuid

from app import db
from app.models.mixins import TimestampMixin, LogMixin


class Anexo(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    caminho_arquivo = db.Column(db.Text, nullable=False)

    relatorio_projeto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('relatorio_coordenador.id'))
    relatorio_bolsista_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('relatorio_bolsista.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
