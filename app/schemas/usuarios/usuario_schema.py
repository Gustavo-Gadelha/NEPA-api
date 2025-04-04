from marshmallow import pre_load, validates, ValidationError

from app import argon2
from app.extensions import ma


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        dump_only = ('id', 'ativo', 'autoridade', 'tipo', 'criado_em', 'atualizado_em', 'criado_por', 'atualizado_por')
        load_only = ('senha',)

    @pre_load
    def hash_senha(self, dados, **kwargs):
        if 'senha' in dados:
            dados['senha'] = argon2.generate_password_hash(dados['senha'])

        return dados

    @validates('senha')
    def validate_senha(self, senha, **kwargs):
        if len(senha) < 8:
            raise ValidationError('A senha deve ter no minimo 8 caracteres')
        if not any(c.isdigit() for c in senha):
            raise ValidationError('A senha deve ter pelo menos 1 numero')
        if not any(c.isalpha() for c in senha):
            raise ValidationError('A senha deve te pelo menos 1 letra')

    # @validates('email')
    # def validate_email(self, email, **kwargs):
    #     stmt = db.select(db.exists().where(Usuario.email == email))
    #     if db.session.scalar(stmt):
    #         raise ValidationError('Este email já está em uso')

    # @validates('matricula')
    # def validate_matricula(self, matricula, **kwargs):
    #     stmt = db.select(db.exists().where(Usuario.matricula == matricula))
    #     if db.session.scalar(stmt):
    #         raise ValidationError('Esta matrícula já está em uso')

    # @validates('telefone')
    # def validate_telefone(self, telefone, **kwargs):
    #     stmt = db.select(db.exists().where(Usuario.telefone == telefone))
    #     if db.session.scalar(stmt):
    #         raise ValidationError('Este número de telefone já está em uso')
