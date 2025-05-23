import numpy as np
import random
from strategy.base import SolverStrategy

class CuckooSolver(SolverStrategy):
    def solve(self, problema):
        n = len(problema.pesos)
        ninhos = np.random.randint(2, size=(25, n))
        melhor = None
        for _ in range(100):
            for i in range(25):
                novo = ninhos[i].copy()
                passo = random.randrange(n)
                novo[passo] = 1 - novo[passo]
                if problema.aptidao(novo) > problema.aptidao(ninhos[i]):
                    ninhos[i] = novo
            if random.random() < 0.25:
                fits = np.array([problema.aptidao(n) for n in ninhos])
                piores = np.argsort(fits)[:max(1, int(0.25 * 25))]
                ninhos[piores] = np.random.randint(2, size=(len(piores), n))
            atual = ninhos[np.argmax([problema.aptidao(n) for n in ninhos])]
            if melhor is None or problema.aptidao(atual) > problema.aptidao(melhor):
                melhor = atual.copy()
        return melhor.tolist(), problema.aptidao(melhor)