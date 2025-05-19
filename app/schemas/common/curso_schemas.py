from app.extensions import ma
from app.models import Curso


class CursoInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Curso
        load_instance = True

    nome = ma.auto_field(required=True)
    sigla = ma.auto_field(required=True)


class CursoOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Curso
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    nome = ma.auto_field()
    sigla = ma.auto_field()
    ativo = ma.auto_field()
