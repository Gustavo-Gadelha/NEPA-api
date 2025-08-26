from flask_jwt_extended import current_user
from flask_smorest import Blueprint
from werkzeug.exceptions import Forbidden

from app.jwt import requires_any
from app.models import ControleMensal, Projeto, Usuario
from app.models.enums import Autoridade

from .schemas import ControleMensalArgsSchema, ControleMensalInSchema, ControleMensalOutSchema

controle_blp = Blueprint('controles', __name__, description='Modulo de controles mensais de frequências')


@controle_blp.get('/')
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
@controle_blp.arguments(ControleMensalArgsSchema, location='query', as_kwargs=True)
@controle_blp.response(200, ControleMensalOutSchema(many=True))
def get_all_controle_mensal(**kwargs):
    if Usuario.access.is_admin():
        return ControleMensal.objects.filter(**kwargs)

    return ControleMensal.objects.filter(**kwargs, professor_id=current_user.id)


@controle_blp.post('/')
@requires_any(Autoridade.PROFESSOR)
@controle_blp.arguments(ControleMensalInSchema)
@controle_blp.response(201, ControleMensalOutSchema)
def post_controle_mensal(controle_mensal):
    projeto = Projeto.objects.get_or_404(controle_mensal.projeto_id)

    if not Usuario.access.is_owner(projeto.professor_id):
        raise Forbidden('Este professor não pode acessar este controle mensal')

    controle_mensal.professor_id = current_user.id
    return ControleMensal.objects.save(controle_mensal)


@controle_blp.get('/<uuid:controle_id>')
@requires_any(Autoridade.ADMIN, Autoridade.PROFESSOR)
@controle_blp.response(200, ControleMensalOutSchema)
def get_controle_mensal(controle_id):
    controle_mensal = ControleMensal.objects.get_or_404(controle_id)

    if not Usuario.access.is_admin() and not Usuario.access.is_owner(controle_mensal.professor_id):
        raise Forbidden('Este professor não pode acessar este controle mensal')

    return controle_mensal


@controle_blp.delete('/<uuid:controle_id>')
@requires_any(Autoridade.PROFESSOR)
@controle_blp.response(204)
def delete_controle_mensal(controle_id):
    controle_mensal = ControleMensal.objects.get_or_404(controle_id)

    if Usuario.access.is_owner(controle_mensal.professor_id):
        raise Forbidden('Este professor não pode acessar este controle mensal')

    ControleMensal.objects.delete(controle_mensal)
