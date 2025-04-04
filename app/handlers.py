from flask import jsonify, Flask
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.exceptions import NotFound, Unauthorized, Forbidden

from app import db


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error: SQLAlchemyError):
        db.session.rollback()
        db.session.close()
        return jsonify({'message': 'Erro de operação no dados do banco', 'error': str(error)}), 500

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error: IntegrityError):
        db.session.rollback()
        db.session.close()
        return jsonify({'message': 'Erro de integridade no banco de dados', 'error': str(error)}), 400

    @app.errorhandler(NotFound)
    def handle_not_found_error(error: NotFound):
        return jsonify({'message': 'Recurso não encontrado', 'error': error.description}), 404

    @app.errorhandler(Unauthorized)
    def handle_unauthorized_error(error: Unauthorized):
        return jsonify({'message': 'Acesso não autorizado', 'error': error.description}), 401

    @app.errorhandler(Forbidden)
    def handle_forbidden_error(error: Forbidden):
        return jsonify({'message': 'Acesso proibido', 'error': error.description}), 403

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({'message': 'Erro de validação', 'errors': error.messages}), 422

    @app.errorhandler(Exception)
    def handle_generic_error(error: Exception):
        return jsonify({'message': 'Erro inesperado ao processar a solicitação', 'error': str(error)}), 500
