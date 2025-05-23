from strategy.ga import GASolver
from strategy.aco import ACOSolver
from strategy.pso import PSOSolver
from strategy.cuckoo import CuckooSolver
from strategy.bee import BeeSolver
from strategy.bat import BatSolver
from strategy.firefly import FireflySolver
from strategy.woa import WOASolver

from core.runner import run_benchmark

solvers = {
    "GA": GASolver(),
    "ACO": ACOSolver(),
    "PSO": PSOSolver(),
    "Cuckoo": CuckooSolver(),
    "Bee": BeeSolver(),
    "Bat": BatSolver(),
    "Firefly": FireflySolver(),
    "WOA": WOASolver(),
}

if __name__ == "__main__":
    ns = [1500, 10000]
    run_benchmark(ns, solvers)
