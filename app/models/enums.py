from enum import Enum


class Autoridade(Enum):
    ADMIN = 'Admin'
    ALUNO = 'Aluno'
    PROFESSOR = 'Professor'


class Situacao(Enum):
    FINALIZADO = 'Finalizado'
    EM_ANDAMENTO = 'Em Andamento'
    APROVADO = 'Aprovado'
    PENDENTE = 'Pendente'
    REJEITADO = 'Rejeitado'
    CANCELADO = 'Cancelado'


class TipoRelatorio(Enum):
    FINAL = 'Final'
    SEMESTRAL = 'Semestral'


class TipoProjeto(Enum):
    PESQUISA = 'Pesquisa'
    EXTENSAO = 'Extensao'
