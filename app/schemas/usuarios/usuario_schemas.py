from marshmallow import post_load, ValidationError, validates

from app.config import MIN_PASSWORD_LENGTH
from app.extensions import ma, argon2
from app.models import Usuario
from app.models.enums import Autoridade


class UsuarioInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True

    nome = ma.auto_field(required=True)
    matricula = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    senha = ma.auto_field(required=True)
    telefone = ma.auto_field(required=True)

    @validates('senha')
    def validate_senha(self, senha, **kwargs):
        if len(senha) < MIN_PASSWORD_LENGTH:
            raise ValidationError(f'A senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres')
        if not any(c.isdigit() for c in senha):
            raise ValidationError('A senha deve ter pelo menos 1 número')
        if not any(c.isalpha() for c in senha):
            raise ValidationError('A senha deve ter pelo menos 1 letra')

    @post_load
    def hash_senha(self, schema, **kwargs):
        schema['senha'] = argon2.generate_password_hash(schema['senha'])  # TODO: deve usar o serviço de usuário
        return schema


class UsuarioOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    nome = ma.auto_field()
    matricula = ma.auto_field()
    email = ma.auto_field()
    telefone = ma.auto_field()
    ativo = ma.auto_field()
    autoridade = ma.Enum(Autoridade, by_value=True, required=True)
    tipo = ma.auto_field()
