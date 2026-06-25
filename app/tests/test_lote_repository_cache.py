import json
import pytest

from unittest.mock import MagicMock
from app.repositories.LoteRepositoryCached import LoteRepositoryCached
from app.models.Lote import Lote
from app.models.Galpao import Galpao
from app.schemas.LoteSchema import LoteBaseSchema
import json

class TestLoteRepositoryCached:
    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    @pytest.fixture
    def cached_repo(self, mock_repo):
        repo = LoteRepositoryCached(repo=mock_repo)
        # Mock o cliente redis para não precisar de um servidor real
        repo._redis = MagicMock()
        return repo

    def test_get_lote_cache_hit(self, cached_repo, mock_repo):
        lote_id = 1
        cached_data = {
            "id_lote": 1,
            "id_galpao": 1,
            "data_alojamento": "2026-06-18",
            "status": "Ativo",
            "quantidade_inicial_aves": 1000,
            "ultimo_peso_g": 0.0,
            "consumo_total_racao_kg": 0.0,
            "mortalidade_acumulada": 0
        }
        cached_repo._redis.get.return_value = json.dumps(cached_data)

        result = cached_repo.get_lote(lote_id)

        assert result.id_lote == cached_data["id_lote"]
        assert result.status == cached_data["status"]
        mock_repo.get_lote.assert_not_called()
        cached_repo._redis.get.assert_called_with(f"lote:{lote_id}")

    def test_get_lote_cache_miss(self, cached_repo, mock_repo):
        lote_id = 1
        # Mock do objeto Lote do SQLAlchemy
        lote_mock = MagicMock()
        lote_mock.id_lote = 1
        # O LoteSchema.dump precisa retornar um dict
        # Como o schema está sendo usado no decorator, talvez precise mockar o schema também
        # Mas para simplificar, vamos deixar o teste falhar se não puder serializar, 
        # ou mockar o schema.
        
        mock_repo.get_lote.return_value = lote_mock
        cached_repo._redis.get.return_value = None

        # Vamos mockar o schema para evitar problemas de dependência de banco
        from unittest.mock import patch
        with patch('app.repositories.LoteRepositoryCached.lote_schema') as mock_schema:
            mock_schema.dump.return_value = {"id_lote": 1}
            result = cached_repo.get_lote(lote_id)

        assert result == lote_mock
        mock_repo.get_lote.assert_called_with(lote_id)
        cached_repo._redis.setex.assert_called()