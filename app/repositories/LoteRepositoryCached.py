import json
import redis
from datetime import timedelta

from app.utils.redis_client import get_redis_client
from app.schemas.LoteSchema import LoteBaseSchema
from app.services.logging_service import setup_logger

logger = setup_logger("LoteRepositoryCached")
lote_schema = LoteBaseSchema()

class LoteRepositoryCached:
    def __init__(self, repo):
        self._repo = repo
        self._redis = get_redis_client()
        self._cache_ttl = timedelta(seconds=3600)

    def get_lote(self, id_lote: int):
        cache_key = f"lote:{id_lote}"

        # Cache Hit
        try:
            cached_data = self._redis.get(cache_key)
            if cached_data:
                logger.debug(f"Cache Hit para Lote {id_lote}")
                return lote_schema.load(json.loads(cached_data))
        except redis.RedisError as e:
            logger.warning(f"Erro ao acessar Redis (get): {e}. Fallback para BD.")
        
        # Cache Miss
        logger.debug(f"Cache Miss para Lote {id_lote}. Buscando no BD.")
        lote = self._repo.get_lote(id_lote)
        
        if lote:
            # Serializa e tenta salvar no cache
            try:
                data = lote_schema.dump(lote)
                self._redis.setex(cache_key, self._cache_ttl, json.dumps(data))
            except redis.RedisError as e:
                logger.warning(f"Erro ao acessar Redis (setex): {e}.")
            
        return lote

    def listar_todos(self):
        cache_key = "lotes:all"
        
        try:
            cached_data = self._redis.get(cache_key)
            if cached_data:
                logger.debug("Cache Hit para Listar Lotes")
                return lote_schema.load(json.loads(cached_data), many=True)
        except redis.RedisError as e:
            logger.warning(f"Erro ao acessar Redis (get): {e}. Fallback para BD.")
        
        logger.debug("Cache Miss para Listar Lotes. Buscando no BD.")
        lotes = self._repo.listar_todos()
        
        # Serializa e tenta salvar no cache
        try:
            data = lote_schema.dump(lotes, many=True)
            self._redis.setex(cache_key, self._cache_ttl, json.dumps(data))
        except redis.RedisError as e:
            logger.warning(f"Erro ao acessar Redis (setex): {e}.")
            
        return lotes

    def save(self, lote):
        # Primeiro salva no banco
        result = self._repo.save(lote)
        
        # Invalida o cache para manter consistência
        self._invalidate_cache(lote.id_lote)
        
        return result

    def delete(self, lote):
        # Primeiro deleta do banco
        id_lote = lote.id_lote
        result = self._repo.delete(lote)
        
        # Invalida o cache
        if result:
            self._invalidate_cache(id_lote)
            
        return result

    def _invalidate_cache(self, id_lote):
        try:
            self._redis.delete(f"lote:{id_lote}")
            self._redis.delete("lotes:all")
            logger.debug(f"Cache invalidado para Lote {id_lote}")
        except redis.RedisError as e:
            logger.warning(f"Erro ao acessar Redis (delete): {e}.")