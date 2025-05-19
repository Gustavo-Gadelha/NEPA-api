from app.extensions import ma
from app.models import Edital


class EditalInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Edital
        load_instance = True

    nome = ma.auto_field(required=True)
    descricao = ma.auto_field(required=True)
    caminho_arquivo = ma.auto_field(required=True)
    admin_id = ma.auto_field(required=True)


class EditalOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Edital
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    nome = ma.auto_field()
    descricao = ma.auto_field()
    caminho_arquivo = ma.auto_field()
    slug = ma.auto_field()
