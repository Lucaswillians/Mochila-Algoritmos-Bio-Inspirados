from strategy.ga import GASolver
from core.problem import ProblemaMochila
import numpy as np

def test_ga_solver_returns_valid_solution():
    pesos = [10, 20, 30, 40]
    valores = [60, 100, 120, 240]
    capacidade = 50
    problema = ProblemaMochila(pesos, valores, capacidade)

    solver = GASolver()
    solucao, valor = solver.solve(problema)

    assert isinstance(solucao, list)
    assert isinstance(valor, (int, float, np.integer, np.floating))  # ✅ Aqui

