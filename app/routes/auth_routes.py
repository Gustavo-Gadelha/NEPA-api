from flask import request, jsonify
from flask_smorest import Blueprint
from werkzeug.exceptions import BadRequest

from app.services import auth_service
from app.services.usuarios import professor_service, aluno_service

auth_bp = Blueprint('auth', __name__, description='Rotas de autenticação')


@auth_bp.route('/login', methods=['POST'])
@auth_bp.response(200)
def auth_login():
    dados = request.json
    login = dados.get('login')
    senha = dados.get('senha')

    usuario = auth_service.login(login, senha)

    if not usuario:
        return jsonify({'message': 'Login ou senha inválidos'}), 401
    if not usuario.ativo:
        return jsonify({'message': 'Usuario não está ativo'}), 403

    access_token = auth_service.access_token(usuario)
    refresh_token = auth_service.refresh_token(usuario)

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


@auth_bp.route('/cadastrar', methods=['POST'])
@auth_bp.response(200)
def auth_register():
    dados = request.json
    tipo = dados.get('tipo', '')

    match tipo.lower():
        case 'aluno':
            aluno_service.save(dados)
        case 'professor':
            professor_service.save(dados)
        case 'admin':
            raise BadRequest('Admins são cadastrados diretamente no banco')
        case _:
            raise BadRequest('Tipo de usuário fornecido é inválido para cadastro')

    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 200
