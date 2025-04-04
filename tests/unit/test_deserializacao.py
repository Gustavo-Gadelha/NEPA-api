from app.schemas import *


def test_curso_deserialization():
    payload = {
        'nome': 'Curso de Teste',
        'sigla': 'CT'
    }
    obj = curso_schema.load(payload)
    assert obj.nome == payload['nome']
    assert obj.sigla == payload['sigla']


def test_admin_deserialization():
    payload = {
        'nome': 'Admin Teste',
        'matricula': 'ADM0001',
        'email': 'admin@teste.com',
        'senha': 'senha_segura',
        'telefone': '999999999'
    }
    obj = admin_schema.load(payload)
    assert obj.nome == payload['nome']
    assert obj.email == payload['email']


def test_aluno_deserialization(curso):
    payload = {
        'nome': 'Aluno Teste',
        'matricula': 'ALN0001',
        'email': 'aluno@teste.com',
        'senha': 'senha_segura',
        'telefone': '988888888',
        'curso_id': str(curso.id)
    }
    obj = aluno_schema.load(payload)
    assert obj.nome == payload['nome']
    assert obj.email == payload['email']


def test_professor_deserialization(curso):
    payload = {
        'nome': 'Professor Teste',
        'matricula': 'PRF0001',
        'email': 'professor@teste.com',
        'senha': 'senha_segura',
        'telefone': '977777777',
        'curso_id': str(curso.id)
    }
    obj = professor_schema.load(payload)
    assert obj.nome == payload['nome']
    assert obj.email == payload['email']


def test_edital_deserialization(admin):
    payload = {
        'nome': 'Edital de Teste',
        'descricao': 'Descrição do edital de teste.',
        'arquivo': 'edital_teste.pdf',
        'admin_id': str(admin.id)
    }
    obj = edital_schema.load(payload)
    assert obj.nome == payload['nome']
    assert obj.descricao == payload['descricao']


def test_projeto_deserialization(professor):
    payload = {
        'titulo': 'Projeto de Teste',
        'sumario': 'Sumário do projeto',
        'situacao': 'EM_ANDAMENTO',
        'titulacao': 'Doutor',
        'linha_de_pesquisa': 'Tecnologia',
        'vagas': 20,
        'palavras_chave': 'teste, educação',
        'localizacao': 'Universidade X',
        'populacao': 'Estudantes',
        'objetivo_geral': 'Objetivo geral do projeto',
        'objetivo_especifico': 'Objetivo específico',
        'justificativa': 'Justificativa do projeto',
        'metodologia': 'Metodologia aplicada',
        'cronograma_atividades': 'Cronograma do projeto',
        'referencias': 'Referências do projeto',
        'aceitou_termos': True,
        'professor_id': str(professor.id),
        'curso_id': str(professor.curso.id)
    }
    obj = projeto_schema.load(payload)
    assert obj.titulo == payload['titulo']
    assert obj.vagas == payload['vagas']


def test_aluno_projeto_deserialization(aluno, projeto):
    payload = {
        'aluno_id': str(aluno.id),
        'projeto_id': str(projeto.id),
        'aprovado': True,
        'bolsista': False
    }
    obj = aluno_projeto_schema.load(payload)
    assert obj.aprovado is True
    assert obj.bolsista is False


def test_atividade_deserialization(aluno, projeto):
    payload = {
        'titulo': 'Atividade 1',
        'descricao': 'Descrição da atividade',
        'data_inicio': '2025-04-01',
        'data_fim': '2025-04-30',
        'aluno_id': str(aluno.id),
        'projeto_id': str(projeto.id)
    }
    obj = atividade_schema.load(payload)
    assert obj.titulo == payload['titulo']
    assert obj.descricao == payload['descricao']


def test_controle_mensal_deserialization(projeto):
    payload = {
        'ano': 2025,
        'mes': 3,
        'projeto_id': str(projeto.id)
    }
    obj = controle_mensal_schema.load(payload)
    assert obj.ano == payload['ano']
    assert obj.mes == payload['mes']


def test_frequencia_semanal_deserialization(controle_mensal):
    payload = {
        'realizada_em': '2025-03-20',
        'tempo_inicio': '14:00:00',
        'tempo_termino': '16:00:00',
        'descricao': 'Reunião semanal',
        'observacao': 'Sem ocorrências',
        'controle_mensal_id': str(controle_mensal.id)
    }
    obj = frequencia_semanal_schema.load(payload)
    assert obj.descricao == payload['descricao']
    assert obj.observacao == payload['observacao']


def test_presenca_deserialization(aluno, frequencia_semanal):
    payload = {
        'aluno_id': str(aluno.id),
        'frequencia_semanal_id': str(frequencia_semanal.id),
        'presente': True,
        'justificativa': None
    }
    obj = presenca_schema.load(payload)
    assert obj.presente is True
