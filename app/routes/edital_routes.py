from pathlib import Path

from flask import request, jsonify, send_file, Blueprint
from flask_jwt_extended import current_user, jwt_required
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app import db
from app.config import UPLOADS_DIR
from app.decorators import requires_any
from app.models import Edital
from app.models.enums import Autoridade
from app.schemas import edital_schema
from app.utils import arquivo_permitido

edital_bp = Blueprint('edital', __name__)


@edital_bp.before_request
@jwt_required()
def checar_usuario():
    if not current_user.ativo:
        return jsonify({'message': 'Acesso negado, usuário não está ativo'}), 401


@edital_bp.route('/', methods=['POST'])
@requires_any(Autoridade.ADMIN)
def criar_edital():
    arquivo: FileStorage | None = request.files.get('file')

    if not arquivo or arquivo.filename == '':
        return jsonify({'message': 'Nenhum arquivo enviado ou selecionado'}), 400
    if not arquivo_permitido(arquivo.filename):
        return jsonify({'message': 'Extensão de arquivo não permitida'}), 400

    nome_arquivo: str = secure_filename(arquivo.filename)
    caminho_arquivo: Path = UPLOADS_DIR / nome_arquivo

    if caminho_arquivo.exists():
        return jsonify({'message': 'Já existe um arquivo com esse nome cadastrado no sistema'}), 409

    caminho_relativo: Path = caminho_arquivo.relative_to(UPLOADS_DIR)

    dados = request.json
    dados.update({'arquivo': caminho_relativo, 'admin_id': current_user.id})

    edital = edital_schema.load(dados)
    db.session.add(edital)
    db.session.commit()

    arquivo.save(caminho_arquivo)

    return jsonify(edital_schema.dump(edital)), 201


@edital_bp.route('/', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def listar_editais():
    editais: list[Edital] | None = db.session.scalars(db.select(Edital).order_by(Edital.id)).all()
    if not editais:
        return jsonify({'message': 'Nenhum edital cadastrado'}), 200

    return jsonify(edital_schema.dump(editais, many=True)), 200


@edital_bp.route('/<uuid:edital_id>', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def exibir_edital_id(edital_id):
    edital: Edital | None = db.session.scalar(db.select(Edital).where(Edital.id == edital_id))
    if not edital:
        return jsonify({'message': 'Edital não encontrado'}), 404

    caminho_arquivo: Path = UPLOADS_DIR / edital.arquivo
    if not caminho_arquivo.exists():
        return jsonify({'message': f'Arquivo não encontrado no caminho: {caminho_arquivo}'}), 404

    return send_file(caminho_arquivo)


@edital_bp.route('/<string:slug>', methods=['GET'])
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
def exibir_edital_slug(slug):
    edital: Edital | None = db.session.scalar(db.select(Edital).where(Edital.slug == slug))
    if not edital:
        return jsonify({'message': 'Edital não encontrado'}), 404

    caminho_arquivo: Path = UPLOADS_DIR / edital.arquivo
    if not caminho_arquivo.exists():
        return jsonify({'message': f'Arquivo não encontrado no caminho: {caminho_arquivo}'}), 404

    return send_file(caminho_arquivo)


@edital_bp.route('/<uuid:edital_id>', methods=['DELETE'])
@requires_any(Autoridade.ADMIN)
def deletar_edital(edital_id):
    edital: Edital | None = db.session.scalar(db.select(Edital).where(Edital.id == edital_id))
    if not edital:
        return jsonify({'message': 'Edital não encontrado'}), 404

    caminho_arquivo: Path = UPLOADS_DIR / edital.arquivo
    if not caminho_arquivo.exists():
        return jsonify({'message': f'Arquivo não encontrado no caminho: {caminho_arquivo}'}), 404

    caminho_arquivo.unlink()
    db.session.delete(edital)
    db.session.commit()

    return jsonify({'message': 'Edital deletado com sucesso'}), 200
