import numpy as np
import random
from strategy.base import SolverStrategy

class GASolver(SolverStrategy):
    def solve(self, problema):
        n_itens = len(problema.pesos)
        tam_pop, geracoes, tx_crossover, tx_mutacao = 50, 100, 0.8, 0.1
        pop = np.random.randint(2, size=(tam_pop, n_itens))
        melhor = None

        for _ in range(geracoes):
            fits = np.array([problema.aptidao(ind) for ind in pop])
            soma = fits.sum()
            probs = fits / soma if soma > 0 else None
            idx_pais = np.random.choice(tam_pop, size=tam_pop, p=probs) if probs is not None else np.random.choice(tam_pop, size=tam_pop)
            nova_pop = pop[idx_pais].copy()

            for i in range(0, tam_pop - 1, 2):
                if random.random() < tx_crossover:
                    ponto = random.randint(1, n_itens - 1)
                    a, b = nova_pop[i].copy(), nova_pop[i + 1].copy()
                    nova_pop[i, ponto:], nova_pop[i + 1, ponto:] = b[ponto:], a[ponto:]

            for i in range(tam_pop):
                for j in range(n_itens):
                    if random.random() < tx_mutacao:
                        nova_pop[i, j] = 1 - nova_pop[i, j]

            pop = nova_pop
            ger_melhor = pop[np.argmax([problema.aptidao(ind) for ind in pop])]
            if melhor is None or problema.aptidao(ger_melhor) > problema.aptidao(melhor):
                melhor = ger_melhor.copy()

        return melhor.tolist(), problema.aptidao(melhor)