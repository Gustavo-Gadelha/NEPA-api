import os
from pathlib import Path

from flask.cli import load_dotenv

BASE_DIR: Path = Path(__file__).parent.parent.resolve()

ENV_PATH: Path = BASE_DIR / '.env'
if not ENV_PATH.exists():
    raise RuntimeError(f'Arquivo .env não encontrado em {ENV_PATH}')

ENV_LOADED: bool = load_dotenv(ENV_PATH)
if not ENV_LOADED:
    raise RuntimeError('As variaveis de ambientes não foram carregadas')

ALLOWED_ANEXOS_EXTENSIONS: set[str] = {'png', 'jpeg', 'jpg'}
ALLOWED_EDITAIS_EXTENSIONS: set[str] = {'pdf', }
MAX_FILE_SIZE: int = 8 * 1024 * 1024  # 8 MB

UPLOADS_DIR: Path = BASE_DIR / 'uploads'
UPLOADS_DIR.mkdir(exist_ok=True)

EDITAIS_DIR: Path = UPLOADS_DIR / 'editais'
EDITAIS_DIR.mkdir(exist_ok=True)

PASSWORD_LENGTH: int = 8


class _Config(object):
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    JWT_SECRET: str = os.getenv('JWT_SECRET')
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_CONTENT_LENGHT', MAX_FILE_SIZE))
    CORS_SUPPORTS_CREDENTIALS: bool = True


class ProductionConfig(_Config):
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv('PRODUCTION_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    CORS_ORIGINS: list[str] = os.getenv('CORS_ORIGINS', '').split(',')

    if not CORS_ORIGINS:
        raise ValueError('Variável CORS_ORIGINS não encontrada ou vazia')


class DevelopmentConfig(_Config):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DEVELOPMENT_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    CORS_ORIGINS: list[str] = ['*']


class TestingConfig(_Config):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv('TEST_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    CORS_ORIGINS: list[str] = ['*']
