from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import fields

from app.extensions import ma
from app.models import Projeto
from app.models.enums import StatusProjeto


class ProjetoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Projeto
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')

    status = EnumField(StatusProjeto, load_by=EnumField.NAME, dump_by=EnumField.VALUE)

    atividades = fields.Nested('AtividadeSchema', many=True, only=('id', 'exibir'))
