import numpy as np
import random
from strategy.base import SolverStrategy

class BeeSolver(SolverStrategy):
    def solve(self, problema):
        n = len(problema.pesos)
        pop = np.random.randint(2, size=(30, n))
        melhor = None
        for _ in range(100):
            fits = np.array([problema.aptidao(ind) for ind in pop])
            idx = np.argsort(-fits)
            nova_pop = []
            for i in idx[:3]:
                site = pop[i]
                for _ in range(5):
                    viz = site.copy()
                    passo = random.randrange(n)
                    viz[passo] = 1 - viz[passo]
                    nova_pop.append(viz)
            while len(nova_pop) < 30:
                nova_pop.append(np.random.randint(2, size=n))
            pop = np.array(nova_pop)
            atual = pop[np.argmax([problema.aptidao(ind) for ind in pop])]
            if melhor is None or problema.aptidao(atual) > problema.aptidao(melhor):
                melhor = atual.copy()
        return melhor.tolist(), problema.aptidao(melhor)
