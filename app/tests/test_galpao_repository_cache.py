import pytest
from unittest.mock import MagicMock
from app.repositories.GalpaoRepositoryCached import GalpaoRepositoryCached
import json

class TestGalpaoRepositoryCached:
    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    @pytest.fixture
    def cached_repo(self, mock_repo):
        repo = GalpaoRepositoryCached(repo=mock_repo)
        # Mock o cliente redis
        repo._redis = MagicMock()
        return repo

    def test_get_by_id_cache_hit(self, cached_repo, mock_repo):
        galpao_id = 1
        cached_data = {"id_galpao": 1, "identificacao": "Galpao A"}
        cached_repo._redis.get.return_value = json.dumps(cached_data)

        result = cached_repo.get_by_id(galpao_id)

        assert result == cached_data
        mock_repo.get_by_id.assert_not_called()
        cached_repo._redis.get.assert_called_with(f"galpao:{galpao_id}")

    def test_get_by_id_cache_miss(self, cached_repo, mock_repo):
        galpao_id = 1
        galpao_mock = MagicMock()
        galpao_mock.id_galpao = 1
        
        mock_repo.get_by_id.return_value = galpao_mock
        cached_repo._redis.get.return_value = None

        from unittest.mock import patch
        with patch('app.repositories.GalpaoRepositoryCached.galpao_schema') as mock_schema:
            mock_schema.dump.return_value = {"id_galpao": 1}
            result = cached_repo.get_by_id(galpao_id)

        assert result == galpao_mock
        mock_repo.get_by_id.assert_called_with(galpao_id)
        cached_repo._redis.setex.assert_called()