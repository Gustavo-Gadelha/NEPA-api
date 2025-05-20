from app.extensions import ma
from app.models import Projeto
from app.models.enums import StatusProjeto


class ProjetoInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Projeto
        load_instance = True

    titulo = ma.auto_field(required=True)
    sumario = ma.auto_field(required=True)
    status = ma.Enum(StatusProjeto, by_value=False, missing=StatusProjeto.PENDENTE)

    titulacao = ma.auto_field(required=True)
    linha_de_pesquisa = ma.auto_field(required=True)

    vagas_ocupadas = ma.auto_field(missing=0)
    vagas_totais = ma.auto_field(required=True)

    palavras_chave = ma.auto_field(required=True)
    localizacao = ma.auto_field(required=True)
    populacao = ma.auto_field(required=True)

    objetivo_geral = ma.auto_field(required=True)
    objetivo_especifico = ma.auto_field(required=True)
    justificativa = ma.auto_field(required=True)
    metodologia = ma.auto_field(required=True)
    cronograma_atividades = ma.auto_field(required=True)
    referencias = ma.auto_field(required=True)

    aceitou_termos = ma.auto_field(required=True)

    professor_id = ma.auto_field(required=True)
    curso_id = ma.auto_field(required=True)


class ProjetoStatusSchema(ma.Schema):
    status = ma.Enum(StatusProjeto, by_value=False)


class ProjetoOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Projeto
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    titulo = ma.auto_field()
    sumario = ma.auto_field()
    status = ma.Enum(StatusProjeto, by_value=True)

    titulacao = ma.auto_field()
    linha_de_pesquisa = ma.auto_field()

    vagas_ocupadas = ma.auto_field()
    vagas_totais = ma.auto_field()

    palavras_chave = ma.auto_field()
    localizacao = ma.auto_field()
    populacao = ma.auto_field()

    objetivo_geral = ma.auto_field()
    objetivo_especifico = ma.auto_field()
    justificativa = ma.auto_field()
    metodologia = ma.auto_field()
    cronograma_atividades = ma.auto_field()
    referencias = ma.auto_field()

    aceitou_termos = ma.auto_field()
    data_limite_edicao = ma.auto_field()

    professor_id = ma.auto_field()
    curso_id = ma.auto_field()
