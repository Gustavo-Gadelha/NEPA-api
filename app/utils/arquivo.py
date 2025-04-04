from app.config import ALLOWED_EDITAIS_EXTENSIONS


def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EDITAIS_EXTENSIONS
