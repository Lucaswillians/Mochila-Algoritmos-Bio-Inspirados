import pytest
from core.problem import ProblemaMochila

def test_aptidao_valida():
    pesos = [10, 20, 30]
    valores = [60, 100, 120]
    capacidade = 50
    problema = ProblemaMochila(pesos, valores, capacidade)

    solucao_valida = [1, 1, 0]  # peso = 30, valor = 160
    assert problema.aptidao(solucao_valida) == 160

def test_aptidao_excede_capacidade():
    pesos = [10, 20, 30]
    valores = [60, 100, 120]
    capacidade = 50
    problema = ProblemaMochila(pesos, valores, capacidade)

    solucao_invalida = [1, 1, 1]  # peso = 60 > capacidade
    assert problema.aptidao(solucao_invalida) == 0
