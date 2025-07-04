from flask_smorest.fields import Upload
from marshmallow import validates, ValidationError
from werkzeug.utils import secure_filename

from app.config import ALLOWED_EDITAIS_EXTENSIONS
from app.extensions import ma
from app.models import Edital


class EditalInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Edital
        load_instance = True

    nome = ma.auto_field(required=True)
    descricao = ma.auto_field(required=True)


class EditalArquivoInSchema(ma.Schema):
    arquivo = Upload(required=True, allow_none=False)

    @validates('arquivo')
    def validate_arquivo(self, arquivo):
        filename = secure_filename(arquivo.filename)
        if '.' not in filename:
            raise ValidationError('Arquivo sem extensão')

        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in ALLOWED_EDITAIS_EXTENSIONS:
            raise ValidationError(f'Extensão não permitida: .{ext}')


class EditalOutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Edital
        include_fk = True

    id = ma.auto_field()
    nome = ma.auto_field()
    descricao = ma.auto_field()
    caminho_arquivo = ma.auto_field()
    slug = ma.auto_field()
