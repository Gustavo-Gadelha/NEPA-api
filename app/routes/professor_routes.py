from flask import request, jsonify, Blueprint
from flask_jwt_extended import current_user, jwt_required

from app import db, argon2
from app.config import PASSWORD_LENGTH
from app.decorators import requires_any
from app.models import Professor
from app.models.enums import Autoridade
from app.schemas import professor_schema

professor_bp = Blueprint('professor', __name__)


@professor_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        return jsonify({'message': 'Acesso negado, usuário não está ativo'}), 401


@professor_bp.route('/', methods=['POST'])
@requires_any(Autoridade.ADMIN)
def criar_professor():
    dados = request.json

    professor = professor_schema.load(dados)
    db.session.add(professor)
    db.session.commit()

    return jsonify(professor_schema.dump(professor)), 201


@professor_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def listar_professores():
    professores: list[Professor] | None = db.session.scalars(db.select(Professor).order_by(Professor.id)).all()
    if not professores:
        return jsonify({'message': 'Nenhum professor cadastrado'}), 200

    return jsonify(professor_schema.dump(professores, many=True)), 200


@professor_bp.route('/<uuid:professor_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def exibir_professor_id(professor_id):
    professor: Professor | None = db.session.scalar(db.select(Professor).where(Professor.id == professor_id))
    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404

    return jsonify(professor_schema.dump(professor)), 200


@professor_bp.route('/<uuid:professor_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
def deletar_professor(professor_id):
    professor: Professor | None = db.session.scalar(db.select(Professor).where(Professor.id == professor_id))
    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404

    db.session.delete(professor)
    db.session.commit()

    return jsonify({'message': 'Professor deletado com sucesso'}), 200


@professor_bp.route('/<uuid:professor_id>/ativar', methods=['POST'])
def ativar_professor(professor_id):
    professor: Professor = db.session.scalar(db.select(Professor).where(Professor.id == professor_id))

    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404
    if professor.ativo:
        return jsonify({'message': 'Este professor já está ativado'}), 200

    professor.ativo = True
    db.session.commit()

    return jsonify(professor_schema.dump(professor)), 200


@professor_bp.route('/<uuid:professor_id>/desativar', methods=['POST'])
def desativar_professor(professor_id):
    professor: Professor = db.session.scalar(db.select(Professor).where(Professor.id == professor_id))

    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404
    if not professor.ativo:
        return jsonify({'message': 'Este professor já está desativado'}), 200

    professor.ativo = False
    db.session.commit()

    return jsonify(professor_schema.dump(professor)), 200


@professor_bp.route('/ativos', methods=['GET'])
def listar_professores_ativos():
    professores: list[Professor] = db.session.scalars(db.select(Professor).where(Professor.ativo == True)).all()

    if not professores:
        return jsonify({'message': 'Nenhum professor ativo encontrado'}), 404

    return jsonify(professor_schema.dump(professores, many=True)), 200


@professor_bp.route('/desativos', methods=['GET'])
def listar_professores_desativos():
    professores: list[Professor] = db.session.scalars(db.select(Professor).where(Professor.ativo == False)).all()

    if not professores:
        return jsonify({'message': 'Nenhum professor não ativo encontrado'}), 404

    return jsonify(professor_schema.dump(professores, many=True)), 200


@professor_bp.route('/<uuid:professor_id>/senha>', methods=['PATCH'])
@requires_any(Autoridade.ADMIN)
def redefinir_senha_professor(professor_id):
    dados = request.json
    senha = dados.get('senha')

    if not senha or len(senha) < PASSWORD_LENGTH:
        return jsonify({'message': f'Senha inválida. A senha deve ter pelo menos {PASSWORD_LENGTH} caracteres'}), 400

    professor = db.session.scalar(db.select(Professor).where(Professor.id == professor_id))

    if not professor:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    professor.senha = argon2.generate_password_hash(senha)
    db.session.commit()

    return jsonify({'message': 'Senha redefinida com sucesso'}), 200
