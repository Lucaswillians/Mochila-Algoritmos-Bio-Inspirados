import pytest
import numbers
from core.problem import ProblemaMochila

from strategy.ga import GASolver
from strategy.pso import PSOSolver
from strategy.aco import ACOSolver
from strategy.bat import BatSolver
from strategy.bee import BeeSolver
from strategy.cuckoo import CuckooSolver
from strategy.firefly import FireflySolver
from strategy.woa import WOASolver

solvers = [
    ("GA", GASolver),
    ("PSO", PSOSolver),
    ("ACO", ACOSolver),
    ("BAT", BatSolver),
    ("BEE", BeeSolver),
    ("CUCKOO", CuckooSolver),
    ("FIREFLY", FireflySolver),
    ("WOA", WOASolver),
]

@pytest.mark.parametrize("name, SolverClass", solvers)
def test_solver_solution_validity(name, SolverClass):
    pesos = [10, 20, 30, 40]
    valores = [60, 100, 120, 240]
    capacidade = 50
    problema = ProblemaMochila(pesos, valores, capacidade)

    solver = SolverClass()
    solucao, valor = solver.solve(problema)

    assert isinstance(solucao, list), f"{name}: solução não é lista"
    assert all(isinstance(x, int) and x in [0, 1] for x in solucao), f"{name}: solução inválida"

    assert isinstance(valor, numbers.Number), f"{name}: valor retornado não é numérico"

    peso_total = sum(p * s for p, s in zip(pesos, solucao))
    assert peso_total <= capacidade, f"{name}: capacidade excedida ({peso_total} > {capacidade})"
