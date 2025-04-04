from app.extensions import ma
from app.models import AlunoProjeto


class AlunoProjetoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AlunoProjeto
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')
