from flask import request, jsonify, Blueprint
from flask_jwt_extended import current_user, jwt_required
from werkzeug.exceptions import BadRequest, Forbidden

from app import db
from app.decorators import requires_any
from app.models import Projeto, AlunoProjeto
from app.models.enums import Autoridade, Situacao
from app.schemas import projeto_schema, aluno_projeto_schema
from app.services.projeto import projeto_service, aluno_projeto_service

projeto_bp = Blueprint('projeto', __name__)


@projeto_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        raise Forbidden('Acesso negado, usuário não está ativo')

    return None


@projeto_bp.route('/', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
def criar_projeto():
    dados = request.json
    projeto = projeto_service.save(dados, current_user.id, current_user.curso.id)

    return jsonify(projeto_schema.dump(projeto)), 201


@projeto_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.ALUNO)
def listar_projetos():
    projetos: list[Projeto] = projeto_service.get_all()
    return jsonify(projeto_schema.dump(projetos, many=True)), 200


@projeto_bp.route('/me', methods=['GET'])
@requires_any(Autoridade.PROFESSOR)
def listar_projetos_do_usuario():
    projetos: list[Projeto] = projeto_service.get_all_from(current_user.id)
    return jsonify(projeto_schema.dump(projetos, many=True)), 200


@projeto_bp.route('/<uuid:projeto_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.ALUNO)
def exibir_projeto_id(projeto_id):
    projeto: Projeto = projeto_service.get_or_404(projeto_id)
    return jsonify(projeto_schema.dump(projeto)), 200


@projeto_bp.route('/<uuid:projeto_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
def deletar_projeto(projeto_id):
    projeto_service.delete(projeto_id)
    return jsonify({'message': 'Projeto deletado com sucesso'}), 200


@projeto_bp.route('/<uuid:projeto_id>/situacao', methods=['PATCH'])
def mudar_situacao_projeto(projeto_id):
    dados = request.json
    situacao = dados.get('situacao')

    if situacao not in Situacao:
        raise BadRequest('Valor inválido para situação')

    projeto: Projeto = projeto_service.change_situation(projeto_id, Situacao[situacao])
    return jsonify(projeto_schema.dump(projeto)), 200


@projeto_bp.route('/aprovados', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def listar_projetos_aprovados():
    projetos: list[Projeto] = projeto_service.get_all_approved()
    return jsonify(projeto_schema.dump(projetos, many=True)), 200


@projeto_bp.route('/pendentes', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def listar_projetos_pendentes():
    projetos: list[Projeto] = projeto_service.get_all_pending()
    return jsonify(projeto_schema.dump(projetos, many=True)), 200


@projeto_bp.route('/<uuid:projeto_id>/alunos', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def listar_alunos_por_projeto(projeto_id):
    projeto: Projeto = projeto_service.get_or_404(projeto_id)
    return jsonify(aluno_projeto_schema.dump(projeto.alunos, many=True)), 200


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>', methods=['POST'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def cadastrar_aluno(projeto_id, aluno_id):
    projeto: Projeto = projeto_service.get_or_404(projeto_id)

    if not projeto.situacao == Situacao.APROVADO:
        return jsonify({'message': 'Este projeto ainda não foi aprovado'}), 403
    if projeto.vagas_totais <= 0:
        return jsonify({'message': 'Não há vagas disponiveis para este projeto'}), 400

    aluno_projeto: AlunoProjeto | None = db.session.scalar(
        db.select(AlunoProjeto).where(AlunoProjeto.projeto_id == projeto_id, AlunoProjeto.aluno_id == aluno_id)
    )

    if aluno_projeto is not None and aluno_projeto.aprovado:
        return jsonify({'message': 'Aluno já está cadastrado e aprovado neste projeto'}), 400
    if aluno_projeto is not None and not aluno_projeto.aprovado:
        return jsonify({'message': 'Aluno já está cadastrado e aguardando aprovação neste projeto'}), 400

    if projeto.vagas_ocupadas >= projeto.vagas_totais:
        return jsonify({'message': 'Todas as vagas ofertadas para este projeto, já foram preenchidas'}), 409

    aluno_projeto = aluno_projeto_service.save(aluno_id, projeto_id)
    return jsonify(aluno_projeto_schema.dump(aluno_projeto)), 201


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>/aprovar', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
def aprovar_aluno_no_projeto(projeto_id, aluno_id):
    aluno_projeto = aluno_projeto_service.approve(aluno_id, projeto_id)
    return jsonify(aluno_projeto_schema.dump(aluno_projeto)), 200


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>/rejeitar', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
def alterar_aluno_projeto(projeto_id, aluno_id):
    aluno_projeto = aluno_projeto_service.reject(aluno_id, projeto_id)
    return jsonify(aluno_projeto_schema.dump(aluno_projeto)), 200
