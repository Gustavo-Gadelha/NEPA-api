from pathlib import Path

from flask import jsonify, send_file
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models.enums import Autoridade
from app.schemas import EditalInSchema, EditalOutSchema, EditalFileInSchema
from app.services import edital_service

edital_bp = Blueprint('edital', __name__, description='Rotas que modificam editais')


@edital_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        raise Forbidden('Acesso negado, usuário não está ativo')

    return None


@edital_bp.route('/', methods=['POST'])
@edital_bp.arguments(EditalInSchema)
@edital_bp.arguments(EditalFileInSchema, location='files')
@edital_bp.response(201, EditalOutSchema)
@requires_any(Autoridade.ADMIN)
def criar_edital(arquivo, edital):
    arquivo = arquivo.get('arquivo')
    return edital_service.save(edital, arquivo)


@edital_bp.route('/', methods=['GET'])
@edital_bp.response(200, EditalOutSchema(many=True))
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def listar_editais():
    return edital_service.get_all()


@edital_bp.route('/<uuid:edital_id>', methods=['GET'])
@edital_bp.response(200, content_type="application/octet-stream")
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def exibir_edital_id(edital_id):
    caminho_arquivo: Path = edital_service.abs_path_to(edital_id)
    if not caminho_arquivo.exists():
        return jsonify({'message': f'Arquivo não encontrado no caminho: {caminho_arquivo}'}), 404

    return send_file(caminho_arquivo)


@edital_bp.route('/<string:slug>', methods=['GET'])
@edital_bp.response(200, content_type="application/octet-stream")
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def exibir_edital_slug(slug):
    caminho_arquivo: Path = edital_service.abs_path_to_by_slug(slug)
    if not caminho_arquivo.exists():
        return jsonify({'message': f'Arquivo não encontrado no caminho: {caminho_arquivo}'}), 404

    return send_file(caminho_arquivo)


@edital_bp.route('/<uuid:edital_id>', methods=['DELETE'])
@edital_bp.response(200)
@requires_any(Autoridade.ADMIN)
def deletar_edital(edital_id):
    edital_service.delete(edital_id)
    return jsonify({'message': 'Edital deletado com sucesso'}), 200
