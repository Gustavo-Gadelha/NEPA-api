from flask import send_file
from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import NotFound

from app.jwt import requires_any
from app.models.enums import Autoridade
from .schemas import EditalInSchema, EditalArquivoInSchema, EditalOutSchema
from .services import edital_service

edital_blp = Blueprint('editais', __name__, url_prefix='/editais', description='Modulo de editais')


@edital_blp.route('/')
class EditalList(MethodView):

    @edital_blp.response(200, EditalOutSchema(many=True))
    def get(self):
        return edital_service.get_all()

    @requires_any(Autoridade.ADMIN)
    @edital_blp.arguments(EditalInSchema)
    @edital_blp.response(201, EditalOutSchema)
    def post(self, edital):
        edital.admin_id = current_user.id
        return edital_service.save(edital)


@edital_blp.route('/<uuid:edital_id>')
class EditalDetail(MethodView):

    @edital_blp.response(200)
    def get(self, edital_id):
        edital = edital_service.get_or_404(edital_id)
        arquivo = edital.caminho_abs()
        if not arquivo.exists():
            raise NotFound('O arquivo deste edital não foi encontrado')

        return send_file(arquivo)

    @requires_any(Autoridade.ADMIN)
    @edital_blp.response(204)
    def delete(self, edital_id):
        return edital_service.delete_by_id(edital_id)


@edital_blp.route('/<uuid:edital_id>/arquivo')
class EditalArquivo(MethodView):

    @requires_any(Autoridade.ADMIN)
    @edital_blp.arguments(EditalArquivoInSchema, location='files')
    @edital_blp.response(200, EditalOutSchema)
    def put(self, dados, edital_id):
        arquivo = dados.get('arquivo')
        return edital_service.update_file(edital_id, arquivo)


@edital_blp.route('/<string:slug>')
class EditalSlug(MethodView):

    @edital_blp.response(200)
    def get(self, slug):
        edital = edital_service.get_by_slug_or_404(slug)
        arquivo = edital.caminho_abs()
        if not arquivo.exists():
            raise NotFound('O arquivo deste edital não foi encontrado')

        return send_file(arquivo)
