from marshmallow_sqlalchemy import fields

from app.extensions import ma
from app.models import RelatorioCoordenador


class RelatorioCoordenadorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RelatorioCoordenador
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')

    projeto = fields.Nested('ProjetoSchema', only=('id',))

    anexos = fields.Nested('AnexoSchema', many=True, only=('id',))
    alunos = fields.Nested('ProjetoSchema', many=True, only=('alunos',))
