from .base import (
    LoginInSchema,
    TokensOutSchema,
    RedefinirSenhaInSchema,
)

from .common import (
    CursoInSchema,
    CursoOutSchema
)

from .documentos import (
    EditalInSchema,
    EditalOutSchema,
    EditalFileInSchema,
    RelatorioBolsistaInSchema,
    RelatorioBolsistaOutSchema,
    RelatorioCoordenadorInSchema,
    RelatorioCoordenadorOutSchema
)

from .frequencias import (
    ControleMensalInSchema,
    ControleMensalOutSchema,
    FrequenciaSemanalInSchema,
    FrequenciaSemanalOutSchema,
    PresencaInSchema,
    PresencaOutSchema
)

from .projeto import (
    AtividadeInSchema,
    AtividadeOutSchema,
    InscricaoInSchema,
    InscricaoOutSchema,
    ProjetoInSchema,
    ProjetoOutSchema,
    ProjetoStatusSchema
)

from .usuarios import (
    AdminInSchema,
    AdminOutSchema,
    AlunoInSchema,
    AlunoOutSchema,
    ProfessorInSchema,
    ProfessorOutSchema,
    UsuarioInSchema,
    UsuarioOutSchema
)
