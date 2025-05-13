import random
import time
import numpy as np

pesos = []
valores = []
capacidade = 0
n_itens = 0

def aptidao(solucao):
    peso_total  = np.dot(solucao, pesos)
    valor_total = np.dot(solucao, valores)
    return valor_total if peso_total <= capacidade else 0

def ga_solve(tam_pop=50, geracoes=100, tx_crossover=0.8, tx_mutacao=0.1):
    pop = np.random.randint(2, size=(tam_pop, n_itens))
    melhor = None
    for _ in range(geracoes):
        fits = np.array([aptidao(ind) for ind in pop])
        soma = fits.sum()
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
        ger_melhor = pop[np.argmax([aptidao(ind) for ind in pop])]
        if melhor is None or aptidao(ger_melhor) > aptidao(melhor):
            melhor = ger_melhor.copy()
    return melhor.tolist(), aptidao(melhor)

def aco_solve(feromonios=50, iteracoes=100, alpha=1.0, beta=2.0, rho=0.1, q=1.0):
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
        ph *= (1 - rho)
        for sol, v in zip(solucoes, fits):
            ph += q * v * sol
    return melhor.tolist(), aptidao(melhor)

def pso_solve(particulas=30, iteracoes=100, w=0.5, c1=1.0, c2=1.0):
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
    ninhos_pos = np.random.randint(2, size=(ninhos, n_itens))
    melhor = None
    for _ in range(iteracoes):
        for i in range(ninhos):
            novo = ninhos_pos[i].copy()
            passo = random.randrange(n_itens)
            novo[passo] = 1 - novo[passo]
            if aptidao(novo) > aptidao(ninhos_pos[i]):
                ninhos_pos[i] = novo
        if random.random() < pa:
            fits  = np.array([aptidao(n) for n in ninhos_pos])
            piores = np.argsort(fits)[:max(1, int(pa*ninhos))]
            ninhos_pos[piores] = np.random.randint(2, size=(len(piores), n_itens))
        atual_melhor = ninhos_pos[np.argmax([aptidao(n) for n in ninhos_pos])]
        if melhor is None or aptidao(atual_melhor) > aptidao(melhor):
            melhor = atual_melhor.copy()
    return melhor.tolist(), aptidao(melhor)

def ba_solve(abelhas=30, elites=3, recrutamentos=5, iteracoes=100):
    pop = np.random.randint(2, size=(abelhas, n_itens))
    melhor = None
    for _ in range(iteracoes):
        fits = np.array([aptidao(ind) for ind in pop])
        idx  = np.argsort(-fits)
        nova_pop = []
        for i in idx[:elites]:
            site = pop[i]
            for _ in range(recrutamentos):
                viz = site.copy()
                passo = random.randrange(n_itens)
                viz[passo] = 1 - viz[passo]
                nova_pop.append(viz)
        while len(nova_pop) < abelhas:
            nova_pop.append(np.random.randint(2, size=n_itens))
        pop = np.array(nova_pop)
        atual_melhor = pop[np.argmax([aptidao(ind) for ind in pop])]
        if melhor is None or aptidao(atual_melhor) > aptidao(melhor):
            melhor = atual_melhor.copy()
    return melhor.tolist(), aptidao(melhor)

def bat_solve(bats=30, iteracoes=100, fmin=0.0, fmax=2.0, alpha=0.9, gamma=0.9):
    # Bat Algorithm binário com clipping para evitar overflow (IMPORTANTISSIMO)
    pos   = np.random.rand(bats, n_itens)
    vel   = np.zeros_like(pos)
    freq  = np.zeros(bats)
    A     = np.ones(bats)
    r     = np.random.rand(bats)
    sol_bin = (pos > 0.5).astype(int)
    fit   = np.array([aptidao(sol_bin[i]) for i in range(bats)])
    best_idx = np.argmax(fit)
    best = sol_bin[best_idx].copy()

    for t in range(iteracoes):
        for i in range(bats):
            freq[i] = fmin + (fmax - fmin) * random.random()
            vel[i] += (pos[i] - pos[best_idx]) * freq[i]
            pos[i] += vel[i]
            if random.random() > r[i]:
                pos[i] = best + 0.001 * np.random.randn(n_itens)
            z = np.clip(pos[i], -50, 50)
            prob = 1.0 / (1.0 + np.exp(-z))
            sol = (prob > np.random.rand(n_itens)).astype(int)
            v = aptidao(sol)
            if v > fit[i] and random.random() < A[i]:
                sol_bin[i], fit[i] = sol, v
                A[i] *= alpha
                r[i]  = r[i] * (1 - np.exp(-gamma * t))
        best_idx = np.argmax(fit)
        best = sol_bin[best_idx].copy()

    return best.tolist(), aptidao(best)

def firefly_solve(fireflies=25, iteracoes=100, beta0=1.0, gamma=1.0, alpha=0.2):
    pos = np.random.rand(fireflies, n_itens)
    melhor = None
    for t in range(iteracoes):
        sol_bin = (pos > 0.5).astype(int)
        fit = np.array([aptidao(sol_bin[i]) for i in range(fireflies)])
        idx = np.argmax(fit)
        if melhor is None or fit[idx] > aptidao(melhor):
            melhor = sol_bin[idx].copy()
        for i in range(fireflies):
            for j in range(fireflies):
                if fit[j] > fit[i]:
                    r2 = np.sum((pos[i] - pos[j])**2)
                    beta = beta0 * np.exp(-gamma * r2)
                    pos[i] += beta * (pos[j] - pos[i]) + alpha * (np.random.rand(n_itens) - 0.5)
            pos[i] = np.clip(pos[i], 0, 1)
        alpha *= 0.97
    return melhor.tolist(), aptidao(melhor)

def woa_solve(whales=30, iteracoes=100, b=1.0):
    pos = np.random.rand(whales, n_itens)
    best_cont = None
    for t in range(iteracoes):
        sol_bin = (pos > 0.5).astype(int)
        fit = np.array([aptidao(sol_bin[i]) for i in range(whales)])
        idx = np.argmax(fit)
        if best_cont is None or fit[idx] > aptidao((best_cont > 0.5).astype(int)):
            best_cont = pos[idx].copy()
        a = 2 - 2 * (t / iteracoes)
        for i in range(whales):
            r = random.random()
            A = 2 * a * r - a
            C = 2 * random.random()
            if random.random() < 0.5:
                if abs(A) < 1:
                    pos[i] = best_cont - A * abs(C * best_cont - pos[i])
                else:
                    rand_idx = random.randint(0, whales-1)
                    X_rand = pos[rand_idx]
                    pos[i] = X_rand - A * abs(C * X_rand - pos[i])
            else:
                D = abs(best_cont - pos[i])
                l = random.uniform(-1, 1)
                pos[i] = D * np.exp(b * l) * np.cos(2 * np.pi * l) + best_cont
        pos = np.clip(pos, 0, 1)
    sol = (best_cont > 0.5).astype(int)
    return sol.tolist(), aptidao(sol)

solvers = {
    "GA":      ga_solve,
    "ACO":     aco_solve,
    "PSO":     pso_solve,
    "Cuckoo":  cs_solve,
    "Bee":     ba_solve,
    "Bat":     bat_solve,
    "Firefly": firefly_solve,
    "WOA":     woa_solve
}

def run_benchmark(ns):
    print(f"{'Itens':<8}{'Algoritmo':<10}{'Valor':<8}{'Tempo(s)':<10}")
    for n in ns:
        global pesos, valores, capacidade, n_itens
        pesos      = np.random.randint(1, 100, size=n).tolist()
        valores    = np.random.randint(1, 100, size=n).tolist()
        capacidade = int(sum(pesos) * 0.5)
        n_itens    = n

        print(f"\n--- Testando com {n} itens ---")
        for nome, fn in solvers.items():
            inicio = time.time()
            sol, val = fn()
            tempo = time.time() - inicio
            print(f"{n:<8}{nome:<10}{val:<8}{tempo:<10.4f}")

if __name__ == "__main__":
    ns = [1500, 10000]
    run_benchmark(ns)
