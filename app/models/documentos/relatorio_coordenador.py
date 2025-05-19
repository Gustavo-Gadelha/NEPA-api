import uuid

from app.extensions import db
from app.models.enums import TipoRelatorio, TipoProjeto
from app.models.mixins import TimestampMixin, LogMixin


class RelatorioCoordenador(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = db.Column(db.Date, nullable=False)

    tipo_relatorio = db.Column(db.Enum(TipoRelatorio), nullable=False)
    tipo_projeto = db.Column(db.Enum(TipoProjeto), nullable=False)

    area_tematica = db.Column(db.String(255), nullable=False)
    linha_programatica = db.Column(db.String(255), nullable=True)

    parceiros = db.Column(db.String(255), nullable=True)

    metas_propostas = db.Column(db.Text, nullable=False)
    participacao_eventos = db.Column(db.Text, nullable=True)
    publico_atendido = db.Column(db.Text, nullable=True)
    resultados_alcancados = db.Column(db.Text, nullable=False)

    anexos = db.relationship('Anexo')

    projeto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('projeto.id'), nullable=False)
    projeto = db.relationship('Projeto')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
