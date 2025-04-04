from app.extensions import ma
from app.models import Curso


class CursoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Curso
        include_fk = True
        load_instance = True
        dump_only = ('id', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')
