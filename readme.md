# 📦 Mochila com Algoritmos Bio-Inspirados - Refatoração

Este projeto aplica algoritmos bio-inspirados para resolver o problema da mochila 0/1. Recentemente, o código passou por uma refatoração significativa com foco em **organização, extensibilidade, testabilidade e manutenibilidade**.

---

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

```
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

## 📈 Conclusão

As mudanças aplicadas tornaram o projeto:

- Mais **organizado** (com separação de responsabilidades)
- **Extensível**, permitindo adicionar novos algoritmos facilmente
- **Testável**, com cobertura automatizada
- **Manutenível**, com menor acoplamento entre componentes

O projeto agora está pronto para evoluir de forma sustentável e colaborativa. 🚀


