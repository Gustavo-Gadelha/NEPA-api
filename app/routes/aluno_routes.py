from flask import request, jsonify, Blueprint
from flask_jwt_extended import current_user, jwt_required

from app import db, argon2
from app.config import PASSWORD_LENGTH
from app.decorators import requires_any
from app.models import Aluno
from app.models.enums import Autoridade
from app.schemas import aluno_schema

aluno_bp = Blueprint('aluno', __name__)


@aluno_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        return jsonify({'message': 'Acesso negado, usuário não está ativo'}), 401


@aluno_bp.route('/', methods=['POST'])
@requires_any(Autoridade.ADMIN)
def criar_aluno():
    dados = request.json

    aluno = aluno_schema.load(dados)
    db.session.add(aluno)
    db.session.commit()

    return jsonify(aluno_schema.dump(aluno)), 201


@aluno_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def listar_alunos():
    alunos: list[Aluno] | None = db.session.scalars(db.select(Aluno).order_by(Aluno.id)).all()
    if not alunos:
        return jsonify({'message': 'Nenhum aluno cadastrado'}), 200

    return jsonify(aluno_schema.dump(alunos, many=True)), 200


@aluno_bp.route('/<uuid:aluno_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN)
def exibir_aluno_id(aluno_id):
    aluno: Aluno | None = db.session.scalar(db.select(Aluno).where(Aluno.id == aluno_id))
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    return jsonify(aluno_schema.dump(aluno)), 200


@aluno_bp.route('/<uuid:aluno_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
def deletar_aluno(aluno_id):
    aluno: Aluno | None = db.session.scalar(db.select(Aluno).where(Aluno.id == aluno_id))
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({'message': 'Aluno deletado com sucesso'}), 200


@aluno_bp.route('/<uuid:aluno_id>/senha>', methods=['PATCH'])
@requires_any(Autoridade.ADMIN)
def redefinir_senha_aluno(aluno_id):
    dados = request.json
    senha = dados.get('senha')

    if not senha or len(senha) < PASSWORD_LENGTH:
        return jsonify({'message': f'Senha inválida. A senha deve ter pelo menos {PASSWORD_LENGTH} caracteres'}), 400

    aluno = db.session.scalar(db.select(Aluno).where(Aluno.id == aluno_id))

    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    aluno.senha = argon2.generate_password_hash(senha)
    db.session.commit()

    return jsonify({'message': 'Senha redefinida com sucesso'}), 200
