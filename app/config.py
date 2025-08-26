import os
from pathlib import Path
from typing import Any

from flask.cli import load_dotenv

BASE_DIR: Path = Path(__file__).parent.parent.resolve()

UPLOADS_DIR: Path = BASE_DIR / 'uploads'
UPLOADS_DIR.mkdir(exist_ok=True)

EDITAIS_DIR: Path = UPLOADS_DIR / 'editais'
EDITAIS_DIR.mkdir(exist_ok=True)

ENV_PATH = BASE_DIR / '.env'
if not ENV_PATH.exists():
    raise RuntimeError(f'Arquivo .env não encontrado em {ENV_PATH}')
if not load_dotenv(ENV_PATH):
    raise RuntimeError('Variáveis de ambiente não foram carregadas')

ALLOWED_EDITAIS_EXTENSIONS: set[str] = {
    'pdf',
}
ALLOWED_ANEXOS_EXTENSIONS: set[str] = {
    'png',
    'jpeg',
    'jpg',
}
MAX_FILE_SIZE: int = 8 * 1024 * 1024  # 8 MB

MIN_PASSWORD_LENGTH: int = 8


class _Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_CONTENT_LENGTH', MAX_FILE_SIZE))

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: int = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '86400'))  # defaults to 1 day
    JWT_REFRESH_TOKEN_EXPIRES: int = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', '2592000'))  # defaults to 30 days
    JWT_COOKIE_DOMAIN: str = os.getenv('JWT_COOKIE_DOMAIN')

    CORS_SUPPORTS_CREDENTIALS: bool = True

    API_TITLE: str = 'NEPA'
    API_VERSION: str = 'v2'
    OPENAPI_VERSION: str = os.getenv('OPENAPI_VERSION', '3.0.2')


class ProductionConfig(_Config):
    DEBUG: bool = False
    PROPAGATE_EXCEPTIONS: bool = False

    SQLALCHEMY_DATABASE_URI: str = os.getenv('PRODUCTION_DATABASE_URI')

    CORS_RESOURCES: list[str] = os.getenv('CORS_RESOURCES', '/')
    CORS_ORIGINS: list[str] = [origin.strip() for origin in os.getenv('CORS_ORIGINS', '').split(',')]

    OPENAPI_URL_PREFIX: str = None
    OPENAPI_SWAGGER_UI_PATH: str = None
    OPENAPI_SWAGGER_UI_URL: str = None


class DevelopmentConfig(_Config):
    DEBUG: bool = True
    PROPAGATE_EXCEPTIONS: bool = True

    SQLALCHEMY_DATABASE_URI: str = os.getenv('DEVELOPMENT_DATABASE_URI')
    SQLALCHEMY_ECHO: bool = os.getenv('SQLALCHEMY_ECHO')

    CORS_ORIGINS: list[str] = ['*']

    OPENAPI_URL_PREFIX: str = os.getenv('OPENAPI_URL_PREFIX', '/')
    OPENAPI_SWAGGER_UI_PATH: str = os.getenv('OPENAPI_SWAGGER_UI_PATH', '/swagger-ui')
    OPENAPI_SWAGGER_UI_URL: str = os.getenv('OPENAPI_SWAGGER_UI_URL', 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/')

    API_SPEC_OPTIONS: dict[str, Any] = {
        'security': [{'bearerAuth': []}],
        'components': {
            'securitySchemes': {
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT'
                }
            }
        }
    }


class TestingConfig(_Config):
    TESTING: bool = True
    PROPAGATE_EXCEPTIONS: bool = True

    SQLALCHEMY_DATABASE_URI: str = os.getenv('TEST_DATABASE_URI')

    CORS_ORIGINS: list[str] = ['*']
