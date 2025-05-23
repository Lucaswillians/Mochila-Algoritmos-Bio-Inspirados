import numpy as np
import random
from strategy.base import SolverStrategy

class BatSolver(SolverStrategy):
    def solve(self, problema):
        n = len(problema.pesos)
        pos = np.random.rand(30, n)
        vel = np.zeros_like(pos)
        freq = np.zeros(30)
        A = np.ones(30)
        r = np.random.rand(30)
        sol_bin = (pos > 0.5).astype(int)
        fit = np.array([problema.aptidao(sol_bin[i]) for i in range(30)])
        best_idx = np.argmax(fit)
        best = sol_bin[best_idx].copy()

        for t in range(100):
            for i in range(30):
                freq[i] = 2.0 * random.random()
                vel[i] += (pos[i] - pos[best_idx]) * freq[i]
                pos[i] += vel[i]
                if random.random() > r[i]:
                    pos[i] = best + 0.001 * np.random.randn(n)
                z = np.clip(pos[i], -50, 50)
                prob = 1.0 / (1.0 + np.exp(-z))
                sol = (prob > np.random.rand(n)).astype(int)
                v = problema.aptidao(sol)
                if v > fit[i] and random.random() < A[i]:
                    sol_bin[i], fit[i] = sol, v
                    A[i] *= 0.9
                    r[i] *= (1 - np.exp(-0.9 * t))
            best_idx = np.argmax(fit)
            best = sol_bin[best_idx].copy()

        return best.tolist(), problema.aptidao(best)
