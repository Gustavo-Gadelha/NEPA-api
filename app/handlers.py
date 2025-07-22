from datetime import datetime, timezone
from typing import Any

import marshmallow as ma
from flask import jsonify, Flask, Response
from flask_jwt_extended.exceptions import JWTDecodeError
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DataError,
    InterfaceError,
    NoResultFound,
    MultipleResultsFound,
    SQLAlchemyError,
)
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    Conflict,
    Unauthorized,
    Forbidden,
    InternalServerError,
    HTTPException,
    ServiceUnavailable,
    RequestEntityTooLarge,
    UnsupportedMediaType,
    MethodNotAllowed,
)

HTTP_ERROR_MESSAGES = {
    400: 'Requisição inválida',
    401: 'Acesso não autorizado',
    403: 'Acesso proibido',
    404: 'Recurso não encontrado',
    405: 'Método HTTP não permitido',
    409: 'Conflito ao salvar os dados',
    413: 'O payload enviado excede o tamanho máximo permitido',
    415: 'Tipo de mídia não suportado',
    422: 'Erro de validação nos dados enviados',
    500: 'Erro interno do servidor',
    503: 'Serviço temporariamente indisponível',
}


class ErrorSchema(ma.Schema):
    code = ma.fields.Integer(required=False)
    message = ma.fields.String(required=True)
    description = ma.fields.String(required=False)
    errors = ma.fields.Dict(keys=ma.fields.String(), required=False)
    timestamp = ma.fields.DateTime(required=True)


class APIError:
    schema: ErrorSchema = ErrorSchema()

    code: int
    message: str
    description: str | None
    errors: dict[str, Any]
    timestamp: datetime

    def __init__(self, code: int, message: str, description: str = None, errors: dict[str, Any] = None):
        self.code = code
        self.message = message
        self.description = description
        self.errors = errors
        self.timestamp = datetime.now(timezone.utc)

    def response(self) -> tuple[Response, int]:
        error_dict = self.schema.dump(self)
        return jsonify(error_dict), self.code

    @classmethod
    def build(cls, code: int = 500, description: str = None, errors: dict[str, Any] = None) -> 'APIError':
        message = HTTP_ERROR_MESSAGES.get(code, 'Erro inesperado')
        return cls(code=code, message=message, description=description, errors=errors)


def register_error_handlers(app: Flask, db: SQLAlchemy) -> None:
    # 4xx Client Errors
    @app.errorhandler(BadRequest)
    def handle_bad_request(error: BadRequest):
        app.logger.warning('Requisição inválida: %s', error.description)
        return APIError.build(400, description=error.description).response()

    @app.errorhandler(Unauthorized)
    def handle_unauthorized_error(error: Unauthorized):
        app.logger.info('Acesso não autorizado: %s', error.description)
        return APIError.build(401, description=error.description).response()

    @app.errorhandler(Forbidden)
    def handle_forbidden_error(error: Forbidden):
        app.logger.info('Acesso proibido: %s', error.description)
        return APIError.build(403, description=error.description).response()

    @app.errorhandler(NotFound)
    def handle_not_found_error(error: NotFound):
        app.logger.info('Recurso não encontrado: %s', error.description)
        return APIError.build(404, description=error.description).response()

    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error: MethodNotAllowed):
        app.logger.warning('Método HTTP não permitido: %s', error.description)
        return APIError.build(405, description=error.description).response()

    @app.errorhandler(Conflict)
    def handle_conflict_error(error: Conflict):
        app.logger.info('Conflito de dados: %s', error.description)
        return APIError.build(409, description=error.description).response()

    @app.errorhandler(RequestEntityTooLarge)
    def handle_request_entity_too_large(error: RequestEntityTooLarge):
        app.logger.warning('Payload muito grande: %s', error.description)
        return APIError.build(413, description=error.description).response()

    @app.errorhandler(UnsupportedMediaType)
    def handle_unsupported_media_type(error: UnsupportedMediaType):
        app.logger.warning('Tipo de mídia não suportado: %s', error.description)
        return APIError.build(415, description=error.description).response()

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        app.logger.warning('Erro de validação: %s', error.messages)
        return APIError.build(422, errors=error.messages).response()

    # 5xx Server Errors
    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(error: InternalServerError):
        app.logger.exception('Erro interno do servidor: %s', str(error))
        return APIError.build(500).response()

    @app.errorhandler(ServiceUnavailable)
    def handle_service_unavailable(error: ServiceUnavailable):
        app.logger.warning('Serviço temporariamente indisponível: %s', error.description)
        return APIError.build(503).response()

    # SQLAlchemy Errors
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error: IntegrityError):
        db.session.rollback()
        db.session.close()
        app.logger.error('Violação de integridade no banco de dados: %s', str(error))
        return APIError.build(400).response()

    @app.errorhandler(DataError)
    def handle_data_error(error: DataError):
        db.session.rollback()
        db.session.close()
        app.logger.error('Erro nos dados fornecidos ao banco de dados: %s', str(error))
        return APIError.build(400).response()

    @app.errorhandler(OperationalError)
    def handle_operational_error(error: OperationalError):
        db.session.rollback()
        db.session.close()
        app.logger.error('Erro operacional ao acessar o banco de dados: %s', str(error))
        return APIError.build(500).response()

    @app.errorhandler(InterfaceError)
    def handle_interface_error(error: InterfaceError):
        db.session.rollback()
        db.session.close()
        app.logger.error('Erro de interface com o banco de dados: %s', str(error))
        return APIError.build(500).response()

    @app.errorhandler(NoResultFound)
    def handle_no_result_found(error: NoResultFound):
        app.logger.info('Nenhum resultado encontrado para a consulta: %s', str(error))
        return APIError.build(404).response()

    @app.errorhandler(MultipleResultsFound)
    def handle_multiple_results_found(error: MultipleResultsFound):
        app.logger.warning('Mais de um resultado foi encontrado quando apenas um era esperado: %s', str(error))
        return APIError.build(400).response()

    # JWT token exception
    @app.errorhandler(JWTDecodeError)
    def handle_jwt_decode_error(error: JWTDecodeError):
        app.logger.warning('JWTDecodeError: %s', str(error))
        return APIError.build(401).response()

    # Catch-All HTTP & Generic Errors
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        app.logger.warning('HTTPException: %s', str(error))
        return APIError.build(500).response()

    @app.errorhandler(SQLAlchemyError)
    def handle_generic_sqlalchemy_error(error: SQLAlchemyError):
        db.session.rollback()
        db.session.close()
        app.logger.exception('Erro genérico no SQLAlchemy: %s', str(error))
        return APIError.build(500).response()

    @app.errorhandler(Exception)
    def handle_generic_exception(error: Exception):
        app.logger.warning('Exception: %s', str(error))
        return APIError.build(500).response()
