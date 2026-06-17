from flask import Blueprint
from flask_restful import Api

from app.repositories.LoteRepository import LoteRepository
from app.repositories.LoteRepositoryCached import LoteRepositoryCached
from app.repositories.GalpaoRepository import GalpaoRepository

from app.services.LoteService import LoteService
from app.services.GalpaoService import GalpaoService

from app.resources.v1.LoteResource import LoteResource
from app.resources.v1.GalpaoResource import GalpaoResource

v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1_bp)

# ==========================================
# INJEÇÃO DE DEPENDÊNCIAS
# ==========================================

# A. Instanciar os repositórios (acesso a dados)
lote_repo = LoteRepository()
lote_repo_cached = LoteRepositoryCached(repo=lote_repo)
galpao_repo = GalpaoRepository()

# B. Instanciar os serviços base
galpao_service = GalpaoService(galpao_repository=galpao_repo)

# C. Instanciar o serviço orquestrador 
lote_service = LoteService(
    lote_repository=lote_repo_cached, 
    galpao_service=galpao_service
)

# ==========================================
# REGISTRO DAS ROTAS (Endpoints)
# ==========================================

# Rotas para gerir os Lotes
api.add_resource(
    LoteResource, 
    '/lotes',
    '/lotes/<int:id_lote>',
    resource_class_kwargs={'lote_service': lote_service}
)

# Rotas para gerir a infraestrutura dos Galpões
api.add_resource(
    GalpaoResource, 
    '/galpoes',
    '/galpoes/<int:id_galpao>',
    resource_class_kwargs={'galpao_service': galpao_service}
)