from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import fields

from app.extensions import ma
from app.models import Projeto
from app.models.enums import Situacao


class ProjetoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Projeto
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')

    situacao = EnumField(Situacao, load_by=EnumField.NAME, dump_by=EnumField.VALUE)

    alunos = fields.Nested('AlunoProjetoSchema', many=True, only=('id', 'aprovado', 'bolsista'))
    atividades = fields.Nested('AtividadeSchema', many=True, only=('id', 'exibir'))
