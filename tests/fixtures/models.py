import uuid
from datetime import date, time

import pytest

from app.models import *
from app.models.enums import StatusProjeto, StatusInscricao


@pytest.fixture
def curso(db_session):
    curso = Curso(
        id=uuid.uuid4(),
        nome='Curso de Teste',
        sigla='CT'
    )
    db_session.add(curso)
    db_session.commit()
    return curso


@pytest.fixture
def admin(db_session):
    admin = Admin(
        id=uuid.uuid4(),
        nome='Admin Teste',
        matricula='ADM0001',
        email='admin@teste.com',
        senha='senha_segura',
        telefone='999999999',
    )
    db_session.add(admin)
    db_session.commit()
    return admin


@pytest.fixture
def aluno(db_session, curso):
    aluno = Aluno(
        id=uuid.uuid4(),
        nome='Aluno Teste',
        matricula='ALN0001',
        email='aluno@teste.com',
        senha='senha_segura',
        telefone='988888888',
        curso=curso,
    )
    db_session.add(aluno)
    db_session.commit()
    return aluno


@pytest.fixture
def professor(db_session, curso):
    professor = Professor(
        id=uuid.uuid4(),
        nome='Professor Teste',
        matricula='PRF0001',
        email='professor@teste.com',
        senha='senha_segura',
        telefone='977777777',
        curso=curso,
    )
    db_session.add(professor)
    db_session.commit()
    return professor


@pytest.fixture
def edital(admin, db_session):
    edital = Edital(
        id=uuid.uuid4(),
        nome='Edital de Teste',
        descricao='Descrição do edital de teste.',
        caminho_arquivo='edital_teste.pdf',
        admin=admin
    )
    db_session.add(edital)
    db_session.commit()
    return edital


@pytest.fixture
def projeto(db_session, professor, curso):
    projeto = Projeto(
        id=uuid.uuid4(),
        titulo='Projeto de Teste',
        sumario='Sumário do projeto',
        status=StatusProjeto.EM_ANDAMENTO,
        titulacao='Doutor',
        linha_de_pesquisa='Tecnologia',
        vagas_totais=20,
        palavras_chave='teste, educação',
        localizacao='Universidade X',
        populacao='Estudantes',
        objetivo_geral='Objetivo geral do projeto',
        objetivo_especifico='Objetivo específico',
        justificativa='Justificativa do projeto',
        metodologia='Metodologia aplicada',
        cronograma_atividades='Cronograma do projeto',
        referencias='Referências do projeto',
        aceitou_termos=True,
        professor=professor,
        curso=curso
    )
    db_session.add(projeto)
    db_session.commit()
    return projeto


@pytest.fixture
def inscricao(db_session, aluno, projeto):
    relacao = Inscricao(
        id=uuid.uuid4(),
        aluno=aluno,
        projeto=projeto,
        status=StatusInscricao.PENDENTE,
        bolsista=False
    )
    db_session.add(relacao)
    db_session.commit()
    return relacao


@pytest.fixture
def atividade(db_session, aluno, projeto):
    atividade = Atividade(
        id=uuid.uuid4(),
        titulo='Atividade 1',
        descricao='Descrição da atividade',
        data_inicio=date(2025, 4, 1),
        data_fim=date(2025, 4, 30),
        aluno=aluno,
        projeto=projeto
    )
    db_session.add(atividade)
    db_session.commit()
    return atividade


@pytest.fixture
def controle_mensal(db_session, projeto):
    controle = ControleMensal(
        id=uuid.uuid4(),
        ano=2025,
        mes=3,
        projeto=projeto
    )
    db_session.add(controle)
    db_session.commit()
    return controle


@pytest.fixture
def frequencia_semanal(db_session, controle_mensal):
    freq = FrequenciaSemanal(
        id=uuid.uuid4(),
        realizada_em=date(2025, 3, 20),
        tempo_inicio=time(14, 0),
        tempo_termino=time(16, 0),
        descricao='Reunião semanal',
        observacao='Sem ocorrências',
        controle_mensal=controle_mensal
    )
    db_session.add(freq)
    db_session.commit()
    return freq


@pytest.fixture
def presenca(db_session, aluno, frequencia_semanal):
    presenca = Presenca(
        id=uuid.uuid4(),
        aluno=aluno,
        frequencia_semanal=frequencia_semanal,
        presente=True,
        justificativa=None
    )
    db_session.add(presenca)
    db_session.commit()
    return presenca
