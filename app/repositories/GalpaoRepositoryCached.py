import json
import redis
from datetime import timedelta

from app.utils.redis_client import get_redis_client
from app.schemas.GalpaoSchema import GalpaoSchema
from app.services.logging_service import setup_logger

logger = setup_logger("GalpaoRepositoryCached")
galpao_schema = GalpaoSchema()

class GalpaoRepositoryCached:
    def __init__(self, repo):
        self._repo = repo
        self._redis = get_redis_client()
        self._cache_ttl = timedelta(seconds=3600)

    def get_by_id(self, id_galpao: int):
        cache_key = f"galpao:{id_galpao}"
        
        try:
            cached_data = self._redis.get(cache_key)
            if cached_data:
                logger.debug(f"Cache Hit para Galpão {id_galpao}")
                return galpao_schema.load(json.loads(cached_data))
        except redis.RedisError as e:
            logger.warning(f"Erro ao acessar Redis (get): {e}. Fallback para BD.")
        
        logger.debug(f"Cache Miss para Galpão {id_galpao}. Buscando no BD.")
        galpao = self._repo.get_by_id(id_galpao)
        
        if galpao:
            try:
                data = galpao_schema.dump(galpao)
                self._redis.setex(cache_key, self._cache_ttl, json.dumps(data))
            except redis.RedisError as e:
                logger.warning(f"Erro ao acessar Redis (setex): {e}.")
            
        return galpao

    def listar_todos(self):
        cache_key = "galpoes:all"
        
        try:
            cached_data = self._redis.get(cache_key)
            if cached_data:
                logger.debug("Cache Hit para Listar Galpões")
                return galpao_schema.load(json.loads(cached_data), many=True)
        except redis.RedisError as e:
            logger.warning(f"Erro ao acessar Redis (get): {e}. Fallback para BD.")
        
        logger.debug("Cache Miss para Listar Galpões. Buscando no BD.")
        galpoes = self._repo.listar_todos()
        
        try:
            data = galpao_schema.dump(galpoes, many=True)
            self._redis.setex(cache_key, self._cache_ttl, json.dumps(data))
        except redis.RedisError as e:
            logger.warning(f"Erro ao acessar Redis (setex): {e}.")
            
        return galpoes

    def save(self, galpao):
        result = self._repo.save(galpao)
        self._invalidate_cache(galpao.id_galpao)
        return result

    def delete(self, galpao):
        id_galpao = galpao.id_galpao
        result = self._repo.delete(galpao)
        if result:
            self._invalidate_cache(id_galpao)
        return result

    def _invalidate_cache(self, id_galpao):
        try:
            self._redis.delete(f"galpao:{id_galpao}")
            self._redis.delete("galpoes:all")
            logger.debug(f"Cache invalidado para Galpão {id_galpao}")
        except redis.RedisError as e:
            logger.warning(f"Erro ao acessar Redis (delete): {e}.")