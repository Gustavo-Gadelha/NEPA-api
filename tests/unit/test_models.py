def test_admin_criado(admin):
    assert admin.id
    assert admin.nome == 'Admin Teste'
    assert admin.autoridade.name == 'ADMIN'
    assert admin.ativo is True
    assert admin.email == 'admin@teste.com'


def test_aluno_criado(aluno):
    assert aluno.id
    assert aluno.nome == 'Aluno Teste'
    assert aluno.autoridade.name == 'ALUNO'
    assert aluno.ativo is True
    assert aluno.matricula == 'ALN0001'
    assert aluno.curso.nome == 'Curso de Teste'


def test_professor_criado(professor):
    assert professor.id
    assert professor.nome == 'Professor Teste'
    assert professor.autoridade.name == 'PROFESSOR'
    assert professor.ativo is False
    assert professor.telefone.startswith('97')
    assert professor.curso.nome == 'Curso de Teste'


def test_curso_criado(curso):
    assert curso.id
    assert curso.nome == 'Curso de Teste'
    assert curso.sigla == 'CT'
    assert curso.ativo is True


def test_edital_criado(edital):
    assert edital.id
    assert edital.nome == 'Edital de Teste'
    assert edital.descricao == 'Descrição do edital de teste.'
    assert edital.arquivo == 'edital_teste.pdf'
    assert edital.slug.startswith('edital-de-teste')
    assert edital.admin.nome == 'Admin Teste'


def test_projeto_criado(projeto):
    assert projeto.id
    assert projeto.titulo == 'Projeto de Teste'
    assert projeto.vagas == 20
    assert projeto.aceitou_termos is True
    assert projeto.professor.nome == 'Professor Teste'
    assert projeto.curso.nome == 'Curso de Teste'


def test_aluno_projeto_criado(aluno_projeto):
    assert aluno_projeto.id
    assert aluno_projeto.aprovado is True
    assert aluno_projeto.bolsista is False
    assert aluno_projeto.aluno.nome == 'Aluno Teste'
    assert aluno_projeto.projeto.titulo == 'Projeto de Teste'


def test_atividade_criada(atividade):
    assert atividade.id
    assert atividade.titulo == 'Atividade 1'
    assert atividade.data_inicio.month == 4
    assert atividade.aluno.nome == 'Aluno Teste'
    assert atividade.projeto.titulo == 'Projeto de Teste'


def test_controle_mensal_criado(controle_mensal):
    assert controle_mensal.id
    assert controle_mensal.ano == 2025
    assert controle_mensal.mes == 3
    assert controle_mensal.projeto.titulo == 'Projeto de Teste'


def test_frequencia_semanal_criada(frequencia_semanal):
    assert frequencia_semanal.id
    assert frequencia_semanal.realizada_em.year == 2025
    assert frequencia_semanal.tempo_inicio.hour == 14
    assert frequencia_semanal.controle_mensal.ano == 2025


def test_presenca_criada(presenca):
    assert presenca.id
    assert presenca.presente is True
    assert presenca.aluno.nome == 'Aluno Teste'
    assert presenca.frequencia_semanal.realizada_em.month == 3
