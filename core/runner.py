import time
import logging

def run_benchmark(ns, solvers):
    from core.problem import ProblemaMochila
    import numpy as np

    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    logging.info(f"{'Itens':<8}{'Algoritmo':<10}{'Valor':<8}{'Tempo(s)':<10}")
    for n in ns:
        pesos = np.random.randint(1, 100, size=n).tolist()
        valores = np.random.randint(1, 100, size=n).tolist()
        capacidade = int(sum(pesos) * 0.5)
        problema = ProblemaMochila(pesos, valores, capacidade)

        logging.info(f"\n--- Testando com {n} itens ---")
        for nome, solver in solvers.items():
            inicio = time.time()
            solucao, valor = solver.solve(problema)
            tempo = time.time() - inicio
            logging.info(f"{n:<8}{nome:<10}{valor:<8}{tempo:<10.4f}")
