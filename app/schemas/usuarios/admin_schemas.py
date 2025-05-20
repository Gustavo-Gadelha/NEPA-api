from app.extensions import ma
from app.models import Admin


class AdminInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Admin
        load_instance = True

    nome = ma.auto_field(required=True)
    matricula = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    senha = ma.auto_field(required=True)
    telefone = ma.auto_field(required=True)


class AdminOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Admin
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    nome = ma.auto_field()
    matricula = ma.auto_field()
    email = ma.auto_field()
    telefone = ma.auto_field()
    ativo = ma.auto_field()
