import numpy as np
import random
from strategy.base import SolverStrategy

class FireflySolver(SolverStrategy):
    def solve(self, problema):
        n = len(problema.pesos)
        pos = np.random.rand(25, n)
        melhor = None
        alpha = 0.2
        for t in range(100):
            sol_bin = (pos > 0.5).astype(int)
            fit = np.array([problema.aptidao(sol_bin[i]) for i in range(25)])
            idx = np.argmax(fit)
            if melhor is None or fit[idx] > problema.aptidao(melhor):
                melhor = sol_bin[idx].copy()
            for i in range(25):
                for j in range(25):
                    if fit[j] > fit[i]:
                        r2 = np.sum((pos[i] - pos[j]) ** 2)
                        beta = 1.0 * np.exp(-1.0 * r2)
                        pos[i] += beta * (pos[j] - pos[i]) + alpha * (np.random.rand(n) - 0.5)
                pos[i] = np.clip(pos[i], 0, 1)
            alpha *= 0.97
        return melhor.tolist(), problema.aptidao(melhor)