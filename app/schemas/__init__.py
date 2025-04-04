from marshmallow import Schema

from .curso_schema import CursoSchema
from .edital_schema import EditalSchema
from .frequencias import ControleMensalSchema, FrequenciaSemanalSchema, PresencaSchema
from .projeto import AlunoProjetoSchema, AtividadeSchema, ProjetoSchema
from .relatorios import AnexoSchema, RelatorioBolsistaSchema, RelatorioCoordenadorSchema
from .usuarios import AdminSchema, AlunoSchema, ProfessorSchema, UsuarioSchema

curso_schema: Schema = CursoSchema()
edital_schema: Schema = EditalSchema()

controle_mensal_schema: Schema = ControleMensalSchema()
frequencia_semanal_schema: Schema = FrequenciaSemanalSchema()
presenca_schema: Schema = PresencaSchema()

aluno_projeto_schema: Schema = AlunoProjetoSchema()
atividade_schema: Schema = AtividadeSchema()
projeto_schema: Schema = ProjetoSchema()

anexo_schema: Schema = AnexoSchema()
relatorio_bolsista_schema: Schema = RelatorioBolsistaSchema()
relatorio_coordenador_schema: Schema = RelatorioCoordenadorSchema()

admin_schema: Schema = AdminSchema()
aluno_schema: Schema = AlunoSchema()
professor_schema: Schema = ProfessorSchema()
usuario_schema: Schema = UsuarioSchema()
