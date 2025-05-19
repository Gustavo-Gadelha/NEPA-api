from marshmallow_enum import EnumField

from app.extensions import ma
from app.models import Inscricao
from app.models.enums import StatusInscricao


class InscricaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inscricao
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')

    status = EnumField(StatusInscricao, load_by=EnumField.NAME, dump_by=EnumField.VALUE)
