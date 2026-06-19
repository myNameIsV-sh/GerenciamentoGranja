import pytest
from app.schemas.LoteSchema import LoteBaseSchema, LoteReadSchema
from app.models.Lote import Lote
from datetime import date

def test_lote_base_schema_load_conversion():
    data = {
        "id_lote": 1,
        "id_galpao": 1,
        "data_alojamento": "2026-06-18",
        "status": "Ativo",
        "quantidade_inicial_aves": 1000
    }
    schema = LoteBaseSchema()
    result = schema.load(data)
    
    assert isinstance(result, Lote)
    assert result.id_lote == 1
    assert result.data_alojamento == date(2026, 6, 18)

def test_lote_base_schema_excludes_semana_atual():
    data = {
        "id_lote": 1,
        "id_galpao": 1,
        "data_alojamento": "2026-06-18",
        "status": "Ativo",
        "quantidade_inicial_aves": 1000,
        "semana_atual": 1 # Deve falhar na validação do load
    }
    schema = LoteBaseSchema()
    with pytest.raises(Exception): # ValidationError
        schema.load(data)

def test_lote_read_schema_includes_semana_atual():
    # Precisamos de um objeto mock que responda a calcular_idade_em_semanas
    class MockLote:
        def __init__(self):
            self.id_lote = 1
            self.id_galpao = 1
            self.data_alojamento = date(2026, 6, 1)
            self.status = "Ativo"
            self.quantidade_inicial_aves = 1000
            self.ultimo_peso_g = 0.0
            self.consumo_total_racao_kg = 0.0
            self.mortalidade_acumulada = 0
            
        @property
        def calcular_idade_em_semanas(self):
            return 3

    lote = MockLote()
    schema = LoteReadSchema()
    result = schema.dump(lote)
    
    assert "semana_atual" in result
    assert result["semana_atual"] == 3
