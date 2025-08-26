from marshmallow import ValidationError, validate, validates

from app.config import MIN_PASSWORD_LENGTH
from app.extensions import ma
from app.models import Curso

from .services import auth_service


class LoginInSchema(ma.Schema):
    login = ma.String(required=True)
    senha = ma.String(required=True)


class RegisterInSchema(ma.Schema):
    nome = ma.String(required=True)
    matricula = ma.String(required=True)
    email = ma.Email(required=True)
    senha = ma.String(required=True)
    confirmar_senha = ma.String(required=True)
    telefone = ma.String(required=True)
    curso_id = ma.UUID(required=True)
    tipo = ma.String(required=True, validate=validate.OneOf(['aluno', 'professor']))

    @validates('matricula', 'email', 'telefone')
    def is_registered(self, value: str, data_key: str) -> None:
        data_filter = {data_key: value}
        if auth_service.first(**data_filter):
            raise ValidationError(f'O valor "{value}" já está cadastrado no banco')

    @validates('senha')
    def validate_senha(self, senha: str, data_key: str) -> None:
        if len(senha) < MIN_PASSWORD_LENGTH:
            raise ValidationError(f'A senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres')
        if not any(c.isdigit() for c in senha):
            raise ValidationError('A senha deve ter pelo menos 1 número')
        if not any(c.isalpha() for c in senha):
            raise ValidationError('A senha deve ter pelo menos 1 letra')

    @validates('curso_id')
    def valitade_curso_id(self, curso_id: str, data_key: str) -> None:
        if not Curso.objects.exists(curso_id):
            raise ValidationError(f"O curso de id: '{curso_id}' não existe")


class RedefinirSenhaInSchema(ma.Schema):
    usuario_id = ma.UUID(required=True)
    senha = ma.String(required=True)

    @validates('senha')
    def validate_senha(self, value: str, data_key: str) -> None:
        if len(value) < MIN_PASSWORD_LENGTH:
            raise ValidationError(f'A senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres')
        if not any(c.isdigit() for c in value):
            raise ValidationError('A senha deve ter pelo menos 1 número')
        if not any(c.isalpha() for c in value):
            raise ValidationError('A senha deve ter pelo menos 1 letra')


class TokensOutSchema(ma.Schema):
    access_token = ma.String(required=True)
    refresh_token = ma.String(required=True)
