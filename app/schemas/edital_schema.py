from app.extensions import ma
from app.models import Edital


class EditalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Edital
        include_fk = True
        load_instance = True
        dump_only = ('id', 'slug', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')
