from flask import send_file
from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint

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
        arquivo = edital_service.get_filepath(edital)
        return send_file(arquivo)

    @requires_any(Autoridade.ADMIN)
    @edital_blp.response(204)
    def delete(self, edital_id):
        edital_service.delete_file(edital_id)
        return edital_service.delete_by_id(edital_id)


@edital_blp.route('/<uuid:edital_id>/arquivo')
class EditalArquivo(MethodView):

    @requires_any(Autoridade.ADMIN)
    @edital_blp.arguments(EditalArquivoInSchema, location='files')
    @edital_blp.response(200, EditalOutSchema)
    def put(self, edital_id, dados):
        edital = edital_service.get_or_404(edital_id)
        arquivo = dados.get('arquivo')

        slug = edital_service.generate_slug(arquivo.filename)
        caminho_relativo = edital_service.save_file(arquivo, edital.slug)
        return edital_service.update(edital_id, {'slug': slug, 'caminho_arquivo': caminho_relativo})


@edital_blp.route('/<string:slug>')
class EditalSlug(MethodView):

    @edital_blp.response(200)
    def get(self, slug):
        edital = edital_service.get_by_slug_or_404(slug)
        arquivo = edital_service.get_filepath(edital)
        return send_file(arquivo)
