import numpy as np
import random
from strategy.base import SolverStrategy

class ACOSolver(SolverStrategy):
    def solve(self, problema):
        n = len(problema.pesos)
        ph = np.ones(n)
        heur = problema.valores / problema.pesos
        melhor = None
        for _ in range(100):
            solucoes, fits = [], []
            for _ in range(50):
                sol = np.zeros(n, dtype=int)
                rem = problema.capacidade
                for i in range(n):
                    num = (ph[i] ** 1.0) * (heur[i] ** 2.0)
                    prob = num / (1 + num)
                    if random.random() < prob and problema.pesos[i] <= rem:
                        sol[i] = 1
                        rem -= problema.pesos[i]
                v = problema.aptidao(sol)
                solucoes.append(sol); fits.append(v)
                if melhor is None or v > problema.aptidao(melhor):
                    melhor = sol.copy()
            ph *= (1 - 0.1)
            for sol, v in zip(solucoes, fits):
                ph += 1.0 * v * sol
        return melhor.tolist(), problema.aptidao(melhor)