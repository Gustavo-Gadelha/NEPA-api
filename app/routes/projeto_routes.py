from flask import request, jsonify, Blueprint
from flask_jwt_extended import current_user, jwt_required

from app import db
from app.decorators import requires_any
from app.models import Projeto, AlunoProjeto
from app.models.enums import Autoridade, Situacao
from app.schemas import projeto_schema, aluno_projeto_schema

projeto_bp = Blueprint('projeto', __name__)


@projeto_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        return jsonify({'message': 'Acesso negado, usuário não está ativo'}), 401


@projeto_bp.route('/', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
def criar_projeto():
    dados = request.json
    dados.update({'professor_id': current_user.id, 'curso_id': current_user.curso.id})

    projeto = projeto_schema.load(dados)
    db.session.add(projeto)
    db.session.commit()

    return jsonify(projeto_schema.dump(projeto)), 201


@projeto_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.ALUNO)
def listar_projetos():
    projetos: list[Projeto] | None = db.session.scalars(db.select(Projeto).order_by(Projeto.id)).all()
    if not projetos:
        return jsonify({'message': 'Nenhum projeto cadastrado'}), 200

    return jsonify(projeto_schema.dump(projetos, many=True)), 200


@projeto_bp.route('/meus', methods=['GET'])
@requires_any(Autoridade.PROFESSOR)
def listar_projetos_do_usuario():
    projetos: list[Projeto] | None = db.session.scalars(
        db.select(Projeto).order_by(Projeto.id).where(Projeto.professor_id == current_user.id)
    ).all()

    if not projetos:
        return jsonify({'message': 'Nenhum projeto cadastrado para este usuário'}), 200

    return jsonify(projeto_schema.dump(projetos, many=True)), 200


@projeto_bp.route('/<uuid:projeto_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.ALUNO)
def exibir_projeto_id(projeto_id):
    projeto: Projeto | None = db.session.scalar(db.select(Projeto).where(Projeto.id == projeto_id))
    if not projeto:
        return jsonify({'message': 'Projeto não encontrado'}), 404

    return jsonify(projeto_schema.dump(projeto)), 200


@projeto_bp.route('/<uuid:projeto_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
def deletar_projeto(projeto_id):
    projeto: Projeto | None = db.session.scalar(db.select(Projeto).where(Projeto.id == projeto_id))
    if not projeto:
        return jsonify({'message': 'Projeto não encontrado'}), 404

    db.session.delete(projeto)
    db.session.commit()

    return jsonify({'message': 'Projeto deletado com sucesso'}), 200


@projeto_bp.route('/<uuid:projeto_id>/aprovar', methods=['POST'])
def aprovar_projeto(projeto_id):
    projeto = db.session.scalar(db.select(Projeto).where(Projeto.id == projeto_id))

    if not projeto:
        return jsonify({'message': 'Projeto não encontrado'}), 404
    if projeto.situacao == Situacao.APROVADO:
        return jsonify({'message': 'Este projeto já foi aprovado'}), 200

    projeto.situacao = Situacao.APROVADO
    db.session.commit()

    return jsonify(projeto_schema.dump(projeto)), 200


@projeto_bp.route('/<uuid:projeto_id>/rejeitar', methods=['POST'])
def rejeitar_projeto(projeto_id):
    projeto = db.session.scalar(db.select(Projeto).where(Projeto.id == projeto_id))

    if not projeto:
        return jsonify({'message': 'Projeto não encontrado'}), 404
    if projeto.situacao == Situacao.REJEITADO:
        return jsonify({'message': 'Este projeto já foi rejeitado'}), 200

    projeto.situacao = Situacao.REJEITADO
    db.session.commit()

    return jsonify(projeto_schema.dump(projeto)), 200


@projeto_bp.route('/<uuid:projeto_id>/cancelar', methods=['POST'])
def cancelar_projeto(projeto_id):
    projeto = db.session.scalar(db.select(Projeto).where(Projeto.id == projeto_id))

    if not projeto:
        return jsonify({'message': 'Projeto não encontrado'}), 404
    if projeto.situacao == Situacao.CANCELADO:
        return jsonify({'message': 'Este projeto já foi cancelado'}), 200

    projeto.situacao = Situacao.CANCELADO
    db.session.commit()

    return jsonify(projeto_schema.dump(projeto)), 200


@projeto_bp.route('/aprovados', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def listar_projetos_aprovados():
    projetos: list[Projeto] | None = db.session.scalars(db.select(Projeto).where(Projeto.situacao == Situacao.APROVADO))
    if not projetos:
        return jsonify({'message': 'Não existem projetos aprovados'}), 404

    return jsonify(projeto_schema.dump(projetos, many=True)), 200


@projeto_bp.route('/pendentes', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def listar_projetos_pendentes():
    projetos: list[Projeto] | None = db.session.scalars(db.select(Projeto).where(Projeto.situacao == Situacao.PENDENTE))
    if not projetos:
        return jsonify({'message': 'Não existem projetos pendentes'}), 404

    return jsonify(projeto_schema.dump(projetos, many=True)), 200


@projeto_bp.route('/<uuid:projeto_id>/alunos', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def listar_alunos_por_projeto(projeto_id):
    projeto: Projeto | None = db.session.scalar(db.select(Projeto).where(Projeto.id == projeto_id))
    if not projeto:
        return jsonify({'message': 'Projeto não encontrado'}), 404
    if not projeto.alunos:
        return jsonify({'message': 'Nenhum aluno cadastrado neste projeto'}), 404

    return jsonify(aluno_projeto_schema.dump(projeto.alunos, many=True)), 200


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>/aprovar', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
def aprovar_aluno_no_projeto(projeto_id, aluno_id):
    aluno_projeto: AlunoProjeto | None = db.session.scalar(
        db.select(AlunoProjeto).where(AlunoProjeto.aluno_id == aluno_id, AlunoProjeto.projeto_id == projeto_id)
    )

    if not aluno_projeto:
        return jsonify({'message': 'Nenhuma relação encontrada entre esse aluno e o projeto'}), 404
    if aluno_projeto.aprovado:
        return jsonify({'message': 'Aluno já está foi aprovado para este projeto'}), 400

    aluno_projeto.aprovado = True
    db.session.commit()

    return jsonify(aluno_projeto_schema.dump(aluno_projeto)), 200


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>/rejeitar', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
def alterar_aluno_projeto(projeto_id, aluno_id):
    aluno_projeto: AlunoProjeto | None = db.session.scalar(
        db.select(AlunoProjeto).where(AlunoProjeto.aluno_id == aluno_id, AlunoProjeto.projeto_id == projeto_id)
    )

    if not aluno_projeto:
        return jsonify({'message': 'Nenhuma relação encontrada entre esse aluno e o projeto'}), 404
    if aluno_projeto.aprovado:
        return jsonify({'message': 'Aluno já está foi rejeitado para este projeto'}), 400

    aluno_projeto.aprovado = False
    db.session.commit()

    return jsonify(aluno_projeto_schema.dump(aluno_projeto)), 200


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>', methods=['POST'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def cadastrar_aluno(projeto_id, aluno_id):
    projeto: Projeto = db.session.scalar(db.select(Projeto).where(Projeto.id == projeto_id))

    if not projeto:
        return jsonify({'message': 'Projeto não encontrado'}), 404
    if not projeto.situacao == Situacao.APROVADO:
        return jsonify({'message': 'Este projeto ainda não foi aprovado'}), 403
    if projeto.vagas <= 0:
        return jsonify({'message': 'Não há vagas disponiveis para este projeto'}), 400

    aluno_projeto: AlunoProjeto = db.session.scalar(
        db.select(AlunoProjeto).where(AlunoProjeto.projeto_id == projeto_id, AlunoProjeto.aluno_id == aluno_id)
    )

    if aluno_projeto and aluno_projeto.aprovado:
        return jsonify({'message': 'Aluno já está cadastrado e aprovado neste projeto'}), 400
    if not aluno_projeto.aprovado:
        return jsonify({'message': 'Aluno já está cadastrado e aguardando aprovação neste projeto'}), 400

    if projeto.vagas_ocupadas >= projeto.vagas:
        return jsonify({'message': 'Todas as vagas ofertadas para este projeto, já foram preenchidas'}), 409

    cadastro = AlunoProjeto(aluno_id=aluno_id, projeto_id=projeto_id)
    projeto.vagas_ocupadas += 1

    db.session.add(cadastro)
    db.session.commit()

    return jsonify(aluno_projeto_schema.dump(cadastro)), 201
