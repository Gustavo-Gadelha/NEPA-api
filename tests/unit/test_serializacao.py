from app.schemas import *


def test_curso_serialization(curso):
    curso_schema = CursoOutSchema()
    data = curso_schema.dump(curso)
    assert data['nome'] == curso.nome
    assert data['sigla'] == curso.sigla


def test_admin_serialization(edital, admin):
    admin_schema = AdminOutSchema()
    data = admin_schema.dump(admin)
    assert data['nome'] == admin.nome
    assert data['email'] == admin.email
    assert data['email'] == admin.email


def test_aluno_serialization(projeto, inscricao, aluno):
    aluno_schema = AlunoOutSchema()
    data = aluno_schema.dump(aluno)
    assert data['nome'] == aluno.nome
    assert data['email'] == aluno.email


def test_professor_serialization(professor):
    professor_schema = ProfessorOutSchema()
    data = professor_schema.dump(professor)
    assert data['nome'] == professor.nome
    assert data['email'] == professor.email


def test_edital_serialization(edital):
    edital_schema = EditalOutSchema()
    data = edital_schema.dump(edital)
    assert data['nome'] == edital.nome
    assert data['descricao'] == edital.descricao


def test_projeto_serialization(projeto):
    projeto_schema = ProjetoOutSchema()
    data = projeto_schema.dump(projeto)
    assert data['titulo'] == projeto.titulo
    assert data['sumario'] == projeto.sumario
    assert data['status'] == projeto.status.value


def test_inscricao_serialization(inscricao):
    inscricao_schema = InscricaoOutSchema()
    data = inscricao_schema.dump(inscricao)
    assert data['status'] == inscricao.status.value
    assert data['bolsista'] == inscricao.bolsista


def test_atividade_serialization(atividade):
    atividade_schema = AtividadeOutSchema()
    data = atividade_schema.dump(atividade)
    assert data['titulo'] == atividade.titulo
    assert data['descricao'] == atividade.descricao


def test_frequencia_semanal_serialization(frequencia_semanal):
    frequencia_semanal_schema = FrequenciaSemanalOutSchema()
    data = frequencia_semanal_schema.dump(frequencia_semanal)
    assert data['descricao'] == frequencia_semanal.descricao
    assert data['observacao'] == frequencia_semanal.observacao


def test_presenca_serialization(presenca):
    presenca_schema = PresencaOutSchema()
    data = presenca_schema.dump(presenca)
    assert data['presente'] == presenca.presente
