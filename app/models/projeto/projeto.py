import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import func

from app.extensions import db
from app.models.enums import StatusProjeto
from app.models.mixins import LogMixin, TimestampMixin


class Projeto(db.Model, TimestampMixin, LogMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    sumario = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(StatusProjeto), nullable=False)

    titulacao = db.Column(db.String(255), nullable=False)
    linha_de_pesquisa = db.Column(db.String(255), nullable=False)

    vagas_ocupadas = db.Column(db.Integer, nullable=False, default=0)
    vagas_totais = db.Column(db.Integer, nullable=False, default=0)

    palavras_chave = db.Column(db.Text, nullable=False)
    localizacao = db.Column(db.String(255), nullable=False)
    populacao = db.Column(db.String(255), nullable=False)

    objetivo_geral = db.Column(db.Text, nullable=False)
    objetivo_especifico = db.Column(db.Text, nullable=False)
    justificativa = db.Column(db.Text, nullable=False)
    metodologia = db.Column(db.Text, nullable=False)
    cronograma_atividades = db.Column(db.Text, nullable=False)
    referencias = db.Column(db.Text, nullable=False)

    aceitou_termos = db.Column(db.Boolean, nullable=False, default=False)

    inscricoes = db.relationship('Inscricao', back_populates='projeto', cascade='all, delete-orphan')
    atividades = db.relationship('Atividade', back_populates='projeto', cascade='all, delete-orphan')

    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professor.id'), nullable=False)
    professor = db.relationship('Professor', back_populates='projetos_propostos', foreign_keys='Projeto.professor_id')

    curso_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('curso.id'), nullable=False)
    curso = db.relationship('Curso')

    data_limite_edicao = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@db.event.listens_for(Projeto, 'after_insert')
def calcular_data_limite_edicao(mapper, connection, target):
    connection.execute(
        Projeto.__table__.update().
        where(Projeto.id == target.id).
        values(data_limite_edicao=target.criado_em + timedelta(days=7))
    )


@db.event.listens_for(Projeto, 'before_update')
def verificar_limite_edicao(mapper, connection, target):
    data_limite = target.data_limite_edicao.replace(tzinfo=UTC)
    if data_limite < datetime.now(UTC):
        raise ValueError('Este projeto não pode mais ser editado')
