from flask import jsonify
from flask_jwt_extended import current_user
from flask_smorest import Blueprint

from app.extensions import db
from app.jwt import requires_any
from app.models import Projeto, Inscricao
from app.models.enums import Autoridade, StatusProjeto
from app.schemas import ProjetoInSchema, ProjetoOutSchema, InscricaoOutSchema, ProjetoStatusSchema
from app.services import projeto_service, inscricao_service

projeto_bp = Blueprint('projeto', __name__, description='Rotas que modificam professores')


@projeto_bp.route('/', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
@projeto_bp.arguments(ProjetoInSchema)
@projeto_bp.response(201, ProjetoOutSchema)
def criar_projeto(projeto):
    return projeto_service.save(projeto)


@projeto_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.ALUNO)
@projeto_bp.response(200, ProjetoOutSchema(many=True))
def listar_projetos():
    return projeto_service.get_all()


@projeto_bp.route('/me', methods=['GET'])
@requires_any(Autoridade.PROFESSOR)
@projeto_bp.response(200, ProjetoOutSchema(many=True))
def listar_projetos_do_usuario():
    return projeto_service.get_all(Projeto.professor_id == current_user.id)


@projeto_bp.route('/<uuid:projeto_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.ALUNO)
@projeto_bp.response(200, ProjetoOutSchema)
def exibir_projeto_id(projeto_id):
    return projeto_service.get_or_404(projeto_id)


@projeto_bp.route('/<uuid:projeto_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
@projeto_bp.response(200)
def deletar_projeto(projeto_id):
    projeto_service.delete(projeto_id)
    return jsonify({'message': 'Projeto deletado com sucesso'}), 200


@projeto_bp.route('/<uuid:projeto_id>/status', methods=['PATCH'])
@requires_any(Autoridade.ADMIN)
@projeto_bp.arguments(ProjetoStatusSchema)
@projeto_bp.response(200, ProjetoOutSchema)
def alterar_status_projeto(args, projeto_id):
    status = args.get('status')
    return projeto_service.change_situation(projeto_id, status)


@projeto_bp.route('/aprovados', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@projeto_bp.response(200, ProjetoOutSchema(many=True))
def listar_projetos_aprovados():
    return projeto_service.get_all(Projeto.status == StatusProjeto.APROVADO)


@projeto_bp.route('/pendentes', methods=['GET'])
@requires_any(Autoridade.ADMIN)
@projeto_bp.response(200, ProjetoOutSchema(many=True))
def listar_projetos_pendentes():
    return projeto_service.get_all(Projeto.status == StatusProjeto.PENDENTE)


@projeto_bp.route('/<uuid:projeto_id>/alunos', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
@projeto_bp.response(200, InscricaoOutSchema(many=True))
def listar_alunos_por_projeto(projeto_id):
    projeto: Projeto = projeto_service.get_or_404(projeto_id)
    return projeto.alunos


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>', methods=['POST'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
@projeto_bp.response(201, InscricaoOutSchema)
def cadastrar_aluno(projeto_id, aluno_id):
    projeto: Projeto = projeto_service.get_or_404(projeto_id)

    if not projeto.status == StatusProjeto.APROVADO:
        return jsonify({'message': 'Este projeto ainda não foi aprovado'}), 403
    if projeto.vagas_totais <= 0:
        return jsonify({'message': 'Não há vagas disponiveis para este projeto'}), 400

    inscricao: Inscricao | None = db.session.scalar(
        db.select(Inscricao).where(Inscricao.projeto_id == projeto_id, Inscricao.aluno_id == aluno_id)
    )

    if inscricao is not None and inscricao.aprovado:
        return jsonify({'message': 'Aluno já está cadastrado e aprovado neste projeto'}), 400
    if inscricao is not None and not inscricao.aprovado:
        return jsonify({'message': 'Aluno já está cadastrado e aguardando aprovação neste projeto'}), 400

    if projeto.vagas_ocupadas >= projeto.vagas_totais:
        return jsonify({'message': 'Todas as vagas ofertadas para este projeto, já foram preenchidas'}), 409

    return inscricao_service.save(aluno_id, projeto_id)


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>/aprovar', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
@projeto_bp.response(200, InscricaoOutSchema)
def aprovar_aluno_no_projeto(projeto_id, aluno_id):
    return inscricao_service.aprovar(aluno_id, projeto_id)


@projeto_bp.route('/<uuid:projeto_id>/alunos/<uuid:aluno_id>/rejeitar', methods=['POST'])
@requires_any(Autoridade.PROFESSOR)
@projeto_bp.response(200, InscricaoOutSchema)
def alterar_aluno_projeto(projeto_id, aluno_id):
    return inscricao_service.rejeitar(aluno_id, projeto_id)
