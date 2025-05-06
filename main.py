import random
import time
import numpy as np

# Definição do problema (será sobrescrito no benchmark)
pesos      = [2, 3, 4, 5]
valores    = [3, 4, 5, 6]
capacidade = 5
n_itens    = len(pesos)

def aptidao(solucao):
    """
    Calcula a aptidão de uma solução binária:
    soma dos valores se o peso total <= capacidade; caso contrário retorna 0.
    """
    peso_total  = np.dot(solucao, pesos)
    valor_total = np.dot(solucao, valores)
    return valor_total if peso_total <= capacidade else 0

def ga_solve(tam_pop=50, geracoes=100, tx_crossover=0.8, tx_mutacao=0.1):
    """
    Genetic Algorithm:
    - Seleção por roleta
    - Crossover de ponto único
    - Mutação bit-flip
    """
    pop = np.random.randint(2, size=(tam_pop, n_itens))
    melhor = None
    for _ in range(geracoes):
        fits = np.array([aptidao(ind) for ind in pop])
        soma = fits.sum()
        # seleção
        if soma > 0:
            probs = fits / soma
            idx_pais = np.random.choice(tam_pop, size=tam_pop, p=probs)
        else:
            idx_pais = np.random.choice(tam_pop, size=tam_pop)
        nova_pop = pop[idx_pais].copy()
        # crossover
        for i in range(0, tam_pop-1, 2):
            if random.random() < tx_crossover:
                ponto = random.randint(1, n_itens-1)
                a, b = nova_pop[i].copy(), nova_pop[i+1].copy()
                nova_pop[i, ponto:], nova_pop[i+1, ponto:] = b[ponto:], a[ponto:]
        # mutação
        for i in range(tam_pop):
            for j in range(n_itens):
                if random.random() < tx_mutacao:
                    nova_pop[i, j] = 1 - nova_pop[i, j]
        pop = nova_pop
        # atualiza melhor
        ger_melhor = pop[np.argmax([aptidao(ind) for ind in pop])]
        if melhor is None or aptidao(ger_melhor) > aptidao(melhor):
            melhor = ger_melhor.copy()
    return melhor.tolist(), aptidao(melhor)

def aco_solve(feromonios=50, iteracoes=100, alpha=1.0, beta=2.0, rho=0.1, q=1.0):
    """
    Ant Colony Optimization:
    - Construção probabilística com feromônio + heurística valor/peso
    - Atualização de feromônio (evaporação e depósito)
    """
    ph    = np.ones(n_itens)
    heur  = np.array(valores) / np.array(pesos)
    melhor = None
    for _ in range(iteracoes):
        solucoes, fits = [], []
        for _ in range(feromonios):
            sol = np.zeros(n_itens, dtype=int)
            rem = capacidade
            for i in range(n_itens):
                num  = (ph[i]**alpha) * (heur[i]**beta)
                prob = num / (1 + num)
                if random.random() < prob and pesos[i] <= rem:
                    sol[i] = 1
                    rem  -= pesos[i]
            v = aptidao(sol)
            solucoes.append(sol); fits.append(v)
            if melhor is None or v > aptidao(melhor):
                melhor = sol.copy()
        ph *= (1 - rho)  # evaporação
        for sol, v in zip(solucoes, fits):
            ph += q * v * sol  # depósito
    return melhor.tolist(), aptidao(melhor)

def pso_solve(particulas=30, iteracoes=100, w=0.5, c1=1.0, c2=1.0):
    """
    Particle Swarm Optimization:
    - Posições contínuas binarizadas via limiar 0.5
    - Atualização de velocidade com inércia e componentes cognitiva/social
    """
    pos   = np.random.rand(particulas, n_itens)
    vel   = np.zeros_like(pos)
    pbest = pos.copy()
    pval  = np.array([aptidao((pos[i]>0.5).astype(int)) for i in range(particulas)])
    gbest = pbest[np.argmax(pval)].copy()
    for _ in range(iteracoes):
        for i in range(particulas):
            r1, r2 = random.random(), random.random()
            vel[i] = w*vel[i] + c1*r1*(pbest[i]-pos[i]) + c2*r2*(gbest-pos[i])
            pos[i] += vel[i]
            sol = (pos[i] > 0.5).astype(int)
            v = aptidao(sol)
            if v > pval[i]:
                pbest[i], pval[i] = pos[i].copy(), v
                if v > aptidao((gbest>0.5).astype(int)):
                    gbest = pos[i].copy()
    sol = (gbest > 0.5).astype(int)
    return sol.tolist(), aptidao(sol)

def cs_solve(ninhos=25, iteracoes=100, pa=0.25):
    """
    Cuckoo Search:
    - Voo de Lévy simplificado para gerar vizinhanças
    - Abandono de piores ninhos
    """
    ninhos_pos = np.random.randint(2, size=(ninhos, n_itens))
    melhor = None
    for _ in range(iteracoes):
        # vizinhança
        for i in range(ninhos):
            novo = ninhos_pos[i].copy()
            passo = random.randrange(n_itens)
            novo[passo] = 1 - novo[passo]
            if aptidao(novo) > aptidao(ninhos_pos[i]):
                ninhos_pos[i] = novo
        # abandono
        if random.random() < pa:
            fits  = np.array([aptidao(n) for n in ninhos_pos])
            piores = np.argsort(fits)[:max(1, int(pa*ninhos))]
            ninhos_pos[piores] = np.random.randint(2, size=(len(piores), n_itens))
        atual_melhor = ninhos_pos[np.argmax([aptidao(n) for n in ninhos_pos])]
        if melhor is None or aptidao(atual_melhor) > aptidao(melhor):
            melhor = atual_melhor.copy()
    return melhor.tolist(), aptidao(melhor)

def ba_solve(abelhas=30, elites=3, recrutamentos=5, iteracoes=100):
    """
    Bee Algorithm:
    - Recrutamento ao redor de elites
    - Exploradores aleatórios para manter diversidade
    """
    pop = np.random.randint(2, size=(abelhas, n_itens))
    melhor = None
    for _ in range(iteracoes):
        fits = np.array([aptidao(ind) for ind in pop])
        idx  = np.argsort(-fits)
        nova_pop = []
        # elites
        for i in idx[:elites]:
            site = pop[i]
            for _ in range(recrutamentos):
                viz = site.copy()
                passo = random.randrange(n_itens)
                viz[passo] = 1 - viz[passo]
                nova_pop.append(viz)
        # exploradores
        while len(nova_pop) < abelhas:
            nova_pop.append(np.random.randint(2, size=n_itens))
        pop = np.array(nova_pop)
        atual_melhor = pop[np.argmax([aptidao(ind) for ind in pop])]
        if melhor is None or aptidao(atual_melhor) > aptidao(melhor):
            melhor = atual_melhor.copy()
    return melhor.tolist(), aptidao(melhor)

# Dicionário de solvers
solvers = {
    "GA":      ga_solve,
    "ACO":     aco_solve,
    "PSO":     pso_solve,
    "Cuckoo":  cs_solve,
    "Bee":     ba_solve
}

def run_benchmark(ns, pop, iters):
    """
    Executa cada algoritmo para volumes de itens ns,
    usando população/colônia/enxame de tamanho pop
    e iteracoes de iteração.
    """
    resultados = []
    for n in ns:
        # gera nova instância
        global pesos, valores, capacidade, n_itens
        pesos      = np.random.randint(1, 100, size=n).tolist()
        valores    = np.random.randint(1, 100, size=n).tolist()
        capacidade = int(sum(pesos) * 0.5)
        n_itens    = n

        print(f"--- Testando com {n} itens ---")
        for nome, fn in solvers.items():
            inicio = time.time()
            sol, val = fn()
            tempo = time.time() - inicio
            resultados.append({
                "Itens":     n,
                "Algoritmo": nome,
                "Valor":     val,
                "Tempo(s)":  round(tempo, 4)
            })
    return resultados

if __name__ == "__main__":
    ns    = [1000, 10000]
    pop   = 30
    iters = 50

    resultados = run_benchmark(ns, pop, iters)

    # imprime resultados em tabela
    print(f"\n{'Itens':<8}{'Algoritmo':<10}{'Valor':<8}{'Tempo(s)':<10}")
    for r in resultados:
        print(f"{r['Itens']:<8}{r['Algoritmo']:<10}{r['Valor']:<8}{r['Tempo(s)']:<10}")

