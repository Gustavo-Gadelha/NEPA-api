from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from app import argon2, db
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login_usuario():
    dados = request.json
    login = dados.get('login')
    senha = dados.get('senha')

    if not login:
        return jsonify({'message': 'login não encontrado na requisição'}), 400
    if not senha:
        return jsonify({'message': 'Senha não encontrada na requisição'}), 400

    if '@' in login:
        stmt = db.select(Usuario).where(Usuario.email == login)
    else:
        stmt = db.select(Usuario).where(Usuario.matricula == login)

    usuario = db.session.scalar(stmt)

    if not usuario or not argon2.check_password_hash(usuario.senha, senha):
        return jsonify({'message': 'Login ou senha inválidos'}), 401
    if not usuario.ativo:
        return jsonify({'message': 'Usuario não está ativo'}), 403

    access_token = create_access_token(identity=usuario)
    refresh_token = create_refresh_token(identity=usuario)

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
