import pytest
import redis
import os

def test_redis_connection():
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    redis_db = int(os.getenv('REDIS_DB', 0))
    
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
    
    try:
        assert r.ping() is True
    except redis.ConnectionError:
        pytest.fail(f"Could not connect to Redis at {redis_host}:{redis_port}")
    except Exception as e:
        pytest.fail(f"An error occurred while connecting to Redis: {e}")