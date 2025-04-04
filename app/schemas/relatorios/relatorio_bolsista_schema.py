from marshmallow_sqlalchemy import fields

from app.extensions import ma
from app.models import RelatorioBolsista


class RelatorioBolsistaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RelatorioBolsista
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')

    anexos = fields.Nested('AnexoSchema', many=True, only=('id',))
    projeto = fields.Nested('ProjetoSchema', only=('id',))
