from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models.enums import Autoridade
from app.resources.controles import controle_mensal_service
from .schemas import FrequenciaSemanalArgsSchema, FrequenciaSemanalInSchema, FrequenciaSemanalOutSchema
from .services import frequencia_semanal_service

frequencia_blp = Blueprint('frequencias', __name__, description='Modulo de frequências semanais')


@frequencia_blp.route('/')
class FrequenciaList(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @frequencia_blp.arguments(FrequenciaSemanalArgsSchema, location='query', as_kwargs=True)
    @frequencia_blp.response(200, FrequenciaSemanalOutSchema(many=True))
    def get(self, controle_id, **kwargs):
        if current_user.autoridade == Autoridade.ADMIN:
            return frequencia_semanal_service.get_all(controle_mensal_id=controle_id, **kwargs)
        if controle_mensal_service.owns_controle(controle_id, current_user.id):
            return frequencia_semanal_service.get_all(controle_mensal_id=controle_id, **kwargs)

        raise Forbidden

    @requires_any(Autoridade.PROFESSOR)
    @frequencia_blp.arguments(FrequenciaSemanalInSchema)
    @frequencia_blp.response(201, FrequenciaSemanalOutSchema)
    def post(self, frequencia, controle_id):
        if not controle_mensal_service.owns_controle(controle_id, current_user.id):
            raise Forbidden('Este professor não pode acessar esse controle mensal')

        frequencia.controle_mensal_id = controle_id
        return frequencia_semanal_service.save(frequencia)


@frequencia_blp.route('/<uuid:frequencia_id>')
class FrequenciaDetail(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @frequencia_blp.response(200, FrequenciaSemanalOutSchema)
    def get(self, controle_id, frequencia_id):
        if current_user.autoridade == Autoridade.ADMIN:
            return frequencia_semanal_service.get_or_404(frequencia_id)
        if controle_mensal_service.owns_controle(controle_id, current_user.id):
            return frequencia_semanal_service.get_or_404(frequencia_id)

        raise Forbidden

    @requires_any(Autoridade.PROFESSOR)
    @frequencia_blp.response(204)
    def delete(self, controle_id, frequencia_id):
        if not controle_mensal_service.owns_controle(controle_id, current_user.id):
            raise Forbidden('Este professor não pode acessar essa frequência')

        return frequencia_semanal_service.delete_by_id(frequencia_id)
