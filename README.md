# 📦 Mochila com Algoritmos Bio-Inspirados - Refatoração

Este projeto aplica algoritmos bio-inspirados para resolver o problema da mochila 0/1. Recentemente, o código passou por uma refatoração significativa com foco em **organização, extensibilidade, testabilidade e manutenibilidade**.

---

## 👤 Equipe

* Cristian Prochnow
* Gustavo Henrique Dias
* Lucas Willian de Souza Serpa
* Marlon de Souza
* Ryan Gabriel Mazzei Bromati

## ✅ Refatorações Realizadas

### 1. Aplicação do Design Pattern: Strategy

**Antes:**  
Cada algoritmo era implementado de forma acoplada, o que dificultava a manutenção e a adição de novos métodos de solução.

**Depois:**  
Adotamos o **padrão Strategy**, permitindo que cada algoritmo seja encapsulado em sua própria classe, herdando de uma interface comum (`SolverStrategy`).

📂 Criamos a pasta `strategy/` com os seguintes módulos:
- `ga.py`, `pso.py`, `aco.py`, `bee.py`, `bat.py`, `cuckoo.py`, `firefly.py`, `woa.py`
- `base.py` define a interface `SolverStrategy`.

**✔️ Vantagem:** Agora é possível adicionar novos algoritmos com facilidade e trocar estratégias sem modificar o código principal.

---

### 2. Modularização do Projeto

**Estrutura anterior:**

![image](https://github.com/user-attachments/assets/874149d7-4b19-4fd9-8240-95c3ff619a65)


**Estrutura atual com a refatoração:**

![image](https://github.com/user-attachments/assets/88c2e7ac-4a62-4015-a4b4-92373a6b7868)



**✔️ Vantagem:** Melhora a organização, separação de responsabilidades e escalabilidade do projeto, tornado a manutenção mais fácil e rica.

---

### 3. Refatoração do Algoritmo Genético (GA)

O algoritmo genético (`GASolver`) foi reescrito para ser mais robusto e alinhado com boas práticas:

- Uso de `numpy` para operações vetoriais mais rápidas.
- Lógica de seleção, crossover e mutação corrigida e simplificada.
- Correção no controle da melhor solução entre gerações.
- Melhoria na legibilidade e performance.

**✔️ Vantagem:** Mais eficiente, claro e fácil de manter.


**Código anterior:**

![image](https://github.com/user-attachments/assets/658d5489-dab0-47dd-ab97-5c79b10fe98c)

**Código atual:**

```python
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
```


---

### 4. Implementação de Testes Automatizados

Foram criados testes utilizando `pytest`:

- **`test_problem.py`**: Verifica a lógica da classe `ProblemaMochila`.
- **`test_algorithm.py`**: Testa individualmente o algoritmo GA.
- **`test_all_algorithm.py`**: Testa todos os algoritmos listados na pasta `strategy`.

**Coberturas testadas:**
- Tipo e formato das soluções
- Correção dos valores retornados
- Comportamento esperado com diferentes entradas

**✔️ Vantagem:** Garantia de funcionamento dos algoritmos. Facilita futuras mudanças com segurança.

---

## ⚡ Rodando Projeto

### Algoritmo

```shell
$ python main.py

[INFO] Itens   Algoritmo Valor   Tempo(s)  
[INFO] 
--- Testando com 1500 itens ---
[INFO] 1500    GA        39198.0 2.1481    
[INFO] 1500    ACO       48518   14.4099   
[INFO] 1500    PSO       41026   0.1702    
[INFO] 1500    Cuckoo    39172   0.1141    
[INFO] 1500    Bee       42442   0.1428    
[INFO] 1500    Bat       37552   0.3341    
[INFO] 1500    Firefly   38472   1.2465    
[INFO] 1500    WOA       38487   0.0815    
[INFO] 
--- Testando com 10000 itens ---
[INFO] 10000   GA        253077.015.1486   
[INFO] 10000   ACO       314021  72.2385   
[INFO] 10000   PSO       251486  0.5262    
[INFO] 10000   Cuckoo    252081  0.3486    
[INFO] 10000   Bee       256567  0.5048    
[INFO] 10000   Bat       249336  1.4044    
[INFO] 10000   Firefly   252521  4.9931    
[INFO] 10000   WOA       254084  0.3416
```

### Testes

```shell
$ PYTHONPATH=. pytest

====================================== test session starts ======================================
platform linux -- Python 3.10.12, pytest-8.3.5, pluggy-1.6.0
rootdir: /home/cristian_prochnow/personal/Mochila-Algoritmos-Bio-Inspirados
collected 11 items                                                                              

tests/test_algorithm.py .                                                                 [  9%]
tests/test_all_algorithm.py ........                                                      [ 81%]
tests/test_problem.py ..                                                                  [100%]

====================================== 11 passed in 0.72s =======================================
```

---

## 📈 Conclusão

As mudanças aplicadas tornaram o projeto:

- Mais **organizado** (com separação de responsabilidades)
- **Extensível**, permitindo adicionar novos algoritmos facilmente
- **Testável**, com cobertura automatizada
- **Manutenível**, com menor acoplamento entre componentes

O projeto agora está pronto para evoluir de forma sustentável e colaborativa. 🚀


