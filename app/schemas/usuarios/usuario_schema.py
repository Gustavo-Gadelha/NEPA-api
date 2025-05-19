from marshmallow import validates, ValidationError, post_load

from app import argon2
from app.extensions import ma


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        dump_only = ('id', 'ativo', 'autoridade', 'tipo', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')
        load_only = ('senha',)

    @validates('senha')
    def validate_senha(self, senha, **kwargs):
        if len(senha) < 8:
            raise ValidationError('A senha deve ter no mínimo 8 caracteres')
        if not any(c.isdigit() for c in senha):
            raise ValidationError('A senha deve ter pelo menos 1 número')
        if not any(c.isalpha() for c in senha):
            raise ValidationError('A senha deve ter pelo menos 1 letra')

    @post_load
    def hash_senha(self, data, **kwargs):
        if 'senha' in data and data['senha']:
            data['senha'] = argon2.generate_password_hash(data['senha'])
        return data
