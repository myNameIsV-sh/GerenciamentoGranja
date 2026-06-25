import os
import redis

def get_redis_client():
    """Retorna uma instância configurada do cliente Redis."""
    return redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0)),
        # docs: if True, the response will be decoded to utf-8
        decode_responses=True
    )