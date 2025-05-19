from app.extensions import ma


class LoginInSchema(ma.Schema):
    login = ma.Email(required=True)
    senha = ma.String(required=True)


class RedefinirSenhaInSchema(ma.Schema):
    senha = ma.String(required=True)


class TokensOutSchema(ma.Schema):
    access_token = ma.String(required=True)
    refresh_token = ma.String(required=True)
