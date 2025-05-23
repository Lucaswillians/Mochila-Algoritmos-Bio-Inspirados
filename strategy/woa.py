import numpy as np
import random
from strategy.base import SolverStrategy

class WOASolver(SolverStrategy):
    def solve(self, problema):
        n = len(problema.pesos)
        pos = np.random.rand(30, n)
        best_cont = None
        for t in range(100):
            sol_bin = (pos > 0.5).astype(int)
            fit = np.array([problema.aptidao(sol_bin[i]) for i in range(30)])
            idx = np.argmax(fit)
            if best_cont is None or fit[idx] > problema.aptidao((best_cont > 0.5).astype(int)):
                best_cont = pos[idx].copy()
            a = 2 - 2 * (t / 100)
            for i in range(30):
                r = random.random()
                A = 2 * a * r - a
                C = 2 * random.random()
                if random.random() < 0.5:
                    if abs(A) < 1:
                        pos[i] = best_cont - A * abs(C * best_cont - pos[i])
                    else:
                        rand_idx = random.randint(0, 29)
                        X_rand = pos[rand_idx]
                        pos[i] = X_rand - A * abs(C * X_rand - pos[i])
                else:
                    D = abs(best_cont - pos[i])
                    l = random.uniform(-1, 1)
                    pos[i] = D * np.exp(1.0 * l) * np.cos(2 * np.pi * l) + best_cont
            pos = np.clip(pos, 0, 1)
        sol = (best_cont > 0.5).astype(int)
        return sol.tolist(), problema.aptidao(sol)