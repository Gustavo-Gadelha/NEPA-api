from app.extensions import ma
from app.models import RelatorioCoordenador
from app.models.enums import TipoRelatorio, TipoProjeto


class RelatorioCoordenadorInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RelatorioCoordenador
        load_instance = True

    data = ma.auto_field(required=True)
    tipo_relatorio = ma.Enum(TipoRelatorio, by_value=False, required=True)
    tipo_projeto = ma.Enum(TipoProjeto, by_value=False, required=True)

    area_tematica = ma.auto_field(required=True)
    linha_programatica = ma.auto_field()
    parceiros = ma.auto_field()

    metas_propostas = ma.auto_field(required=True)
    participacao_eventos = ma.auto_field()
    publico_atendido = ma.auto_field()
    resultados_alcancados = ma.auto_field(required=True)

    projeto_id = ma.auto_field(required=True)


class RelatorioCoordenadorOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RelatorioCoordenador
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    data = ma.auto_field()
    tipo_relatorio = ma.Enum(TipoRelatorio, by_value=True)
    tipo_projeto = ma.Enum(TipoProjeto, by_value=True)

    area_tematica = ma.auto_field()
    linha_programatica = ma.auto_field()
    parceiros = ma.auto_field()

    metas_propostas = ma.auto_field()
    participacao_eventos = ma.auto_field()
    publico_atendido = ma.auto_field()
    resultados_alcancados = ma.auto_field()

    projeto_id = ma.auto_field()
