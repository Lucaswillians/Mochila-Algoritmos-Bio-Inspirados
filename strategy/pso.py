import numpy as np
import random
from strategy.base import SolverStrategy

class PSOSolver(SolverStrategy):
    def solve(self, problema):
        n = len(problema.pesos)
        pos = np.random.rand(30, n)
        vel = np.zeros_like(pos)
        pbest = pos.copy()
        pval = np.array([problema.aptidao((pos[i] > 0.5).astype(int)) for i in range(30)])
        gbest = pbest[np.argmax(pval)].copy()

        for _ in range(100):
            for i in range(30):
                r1, r2 = random.random(), random.random()
                vel[i] = 0.5 * vel[i] + 1.0 * r1 * (pbest[i] - pos[i]) + 1.0 * r2 * (gbest - pos[i])
                pos[i] += vel[i]
                sol = (pos[i] > 0.5).astype(int)
                v = problema.aptidao(sol)
                if v > pval[i]:
                    pbest[i], pval[i] = pos[i].copy(), v
                    if v > problema.aptidao((gbest > 0.5).astype(int)):
                        gbest = pos[i].copy()
        sol = (gbest > 0.5).astype(int)
        return sol.tolist(), problema.aptidao(sol)
