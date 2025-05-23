import numpy as np

class ProblemaMochila:
    def __init__(self, pesos, valores, capacidade):
        self.pesos = np.array(pesos)
        self.valores = np.array(valores)
        self.capacidade = capacidade

    def aptidao(self, solucao):
        peso_total = np.dot(solucao, self.pesos)
        valor_total = np.dot(solucao, self.valores)
        return valor_total if peso_total <= self.capacidade else 0
