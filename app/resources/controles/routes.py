from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models.enums import Autoridade
from app.resources.projetos import projeto_service

from .schemas import ControleMensalArgsSchema, ControleMensalInSchema, ControleMensalOutSchema
from .services import controle_mensal_service

controle_blp = Blueprint('controles', __name__, description='Modulo de controles mensais de frequências')


@controle_blp.route('/')
class ControleList(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @controle_blp.arguments(ControleMensalArgsSchema, location='query', as_kwargs=True)
    @controle_blp.response(200, ControleMensalOutSchema(many=True))
    def get(self, **kwargs):
        if current_user.autoridade == Autoridade.PROFESSOR:
            return controle_mensal_service.get_all(**kwargs, professor_id=current_user.id)

        return controle_mensal_service.get_all(**kwargs)

    @requires_any(Autoridade.PROFESSOR)
    @controle_blp.arguments(ControleMensalInSchema)
    @controle_blp.response(201, ControleMensalOutSchema)
    def post(self, controle_mensal):
        if not projeto_service.owns_project(controle_mensal.projeto_id, current_user.id):
            raise Forbidden('Este professor não pode acessar este controle mensal')

        controle_mensal.professor_id = current_user.id
        return controle_mensal_service.save(controle_mensal)


@controle_blp.route('/<uuid:controle_id>')
class ControleDetail(MethodView):

    @requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
    @controle_blp.response(200, ControleMensalOutSchema)
    def get(self, controle_id):
        if current_user.autoridade == Autoridade.PROFESSOR:
            return controle_mensal_service.one(id=controle_id, professor_id=current_user.id)

        return controle_mensal_service.get_or_404(controle_id)

    @requires_any(Autoridade.PROFESSOR)
    @controle_blp.response(204)
    def delete(self, controle_id):
        if not projeto_service.owns_project(controle_id.projeto_id, current_user.id):
            raise Forbidden('Este professor não pode acessar este controle mensal')

        return controle_mensal_service.delete_by_id(controle_id)
