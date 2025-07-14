from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden, NotFound

from app.jwt import requires_any
from app.models.enums import Autoridade
from app.resources.controles import controle_mensal_service
from app.resources.projetos import projeto_service
from .schemas import FrequenciaSemanalInSchema, FrequenciaSemanalArgsSchema, FrequenciaSemanalOutSchema
from .services import frequencia_semanal_service

frequencia_blp = Blueprint('frequencias', __name__, description='Modulo de frequências semanais')


@frequencia_blp.route('/')
class FrequenciaList(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @frequencia_blp.arguments(FrequenciaSemanalArgsSchema, location='query', as_kwargs=True)
    @frequencia_blp.response(200, FrequenciaSemanalOutSchema(many=True))
    def get(self, controle_id, **kwargs):
        return frequencia_semanal_service.get_all(controle_id=controle_id, **kwargs)

    @requires_any(Autoridade.PROFESSOR)
    @frequencia_blp.arguments(FrequenciaSemanalInSchema)
    @frequencia_blp.response(201, FrequenciaSemanalOutSchema)
    def post(self, frequencia, controle_id):
        if not projeto_service.is_owner(controle_id.projeto_id, current_user.id):
            raise Forbidden

        frequencia.controle_mensal_id = controle_id
        return frequencia_semanal_service.save(frequencia)


@frequencia_blp.route('/<uuid:frequencia_id>')
class FrequenciaDetail(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @frequencia_blp.response(200, FrequenciaSemanalOutSchema)
    def get(self, controle_id, frequencia_id):
        controle_mensal = controle_mensal_service.get_or_404(controle_id)
        frequencia_semanal = frequencia_semanal_service.get_or_404(frequencia_id)

        if frequencia_semanal not in controle_mensal.frequencias_semanais:
            raise NotFound

        return frequencia_semanal

    @requires_any(Autoridade.PROFESSOR)
    @frequencia_blp.response(204)
    def delete(self, controle_id, frequencia_id):
        if not projeto_service.is_owner(controle_id.projeto_id, current_user.id):
            raise Forbidden
        
        return frequencia_semanal_service.delete_by_id(frequencia_id)
