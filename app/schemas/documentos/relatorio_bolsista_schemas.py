from app.extensions import ma
from app.models import RelatorioBolsista
from app.models.enums import TipoRelatorio, TipoProjeto


class RelatorioBolsistaInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RelatorioBolsista
        load_instance = True

    data = ma.auto_field(required=True)
    tipo_relatorio = ma.Enum(TipoRelatorio, by_value=False, required=True)
    tipo_projeto = ma.Enum(TipoProjeto, by_value=False, required=True)

    atividades_desenvolvidas = ma.auto_field()
    dificuldades_encontradas = ma.auto_field()
    pontos_positivos = ma.auto_field()
    autoavaliacao = ma.auto_field()

    projeto_id = ma.auto_field(required=True)


class RelatorioBolsistaOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RelatorioBolsista
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    data = ma.auto_field()
    tipo_relatorio = ma.Enum(TipoRelatorio, by_value=True)
    tipo_projeto = ma.Enum(TipoProjeto, by_value=True)

    atividades_desenvolvidas = ma.auto_field()
    dificuldades_encontradas = ma.auto_field()
    pontos_positivos = ma.auto_field()
    autoavaliacao = ma.auto_field()

    projeto_id = ma.auto_field()
