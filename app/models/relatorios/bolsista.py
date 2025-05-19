import uuid

from app import db
from app.models.enums import TipoRelatorio, TipoProjeto
from app.models.mixins import TimestampMixin, LogMixin


class RelatorioBolsista(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = db.Column(db.Date, nullable=False)

    tipo_relatorio = db.Column(db.Enum(TipoRelatorio), nullable=False)
    tipo_projeto = db.Column(db.Enum(TipoProjeto), nullable=False)

    atividades_desenvolvidas = db.Column(db.Text, nullable=True)
    dificuldades_encontradas = db.Column(db.Text, nullable=True)
    pontos_positivos = db.Column(db.Text, nullable=True)
    autoavaliacao = db.Column(db.Text, nullable=True)

    anexos = db.relationship('Anexo')

    projeto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('projeto.id'), nullable=False)
    projeto = db.relationship('Projeto')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
