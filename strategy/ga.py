import numpy as np
import random
from strategy.base import SolverStrategy
from core.problem import ProblemaMochila
from typing import List, Tuple

class GASolver(SolverStrategy):
    def __init__(self, tam_pop=50, geracoes=100, tx_crossover=0.8, tx_mutacao=0.1):
        self.tam_pop = tam_pop
        self.geracoes = geracoes
        self.tx_crossover = tx_crossover
        self.tx_mutacao = tx_mutacao

    def solve(self, problema: ProblemaMochila) -> Tuple[List[int], float]:
        n_itens = len(problema.pesos)
        pop = np.random.randint(2, size=(self.tam_pop, n_itens))
        melhor = None
        melhor_valor = float('-inf')

        for _ in range(self.geracoes):
            aptidoes = np.array([problema.aptidao(ind) for ind in pop])
            soma = aptidoes.sum()
            probs = aptidoes / soma if soma > 0 else None

            idx_pais = np.random.choice(
                self.tam_pop, size=self.tam_pop, p=probs
            ) if probs is not None else np.random.choice(self.tam_pop, size=self.tam_pop)

            nova_pop = pop[idx_pais].copy()

            for i in range(0, self.tam_pop - 1, 2):
                if random.random() < self.tx_crossover:
                    ponto = random.randint(1, n_itens - 1)
                    nova_pop[i, ponto:], nova_pop[i + 1, ponto:] = (
                        nova_pop[i + 1, ponto:].copy(),
                        nova_pop[i, ponto:].copy()
                    )

            for i in range(self.tam_pop):
                for j in range(n_itens):
                    if random.random() < self.tx_mutacao:
                        nova_pop[i, j] = 1 - nova_pop[i, j]

            pop = nova_pop
            aptidoes = np.array([problema.aptidao(ind) for ind in pop])
            idx_melhor = np.argmax(aptidoes)
            if aptidoes[idx_melhor] > melhor_valor:
                melhor = pop[idx_melhor].copy()
                melhor_valor = aptidoes[idx_melhor]

        return melhor.tolist(), float(melhor_valor)
