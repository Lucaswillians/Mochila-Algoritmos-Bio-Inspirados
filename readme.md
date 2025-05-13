## Relatório de Benchmark: Problema da Mochila 0/1

### 1. Introdução
Este relatório apresenta os resultados de um benchmark comparativo de oito algoritmos bio-inspirados na resolução do Problema da Mochila 0/1, para instâncias de tamanho grande:

- **Instâncias testadas**:  
  - 1500 itens  
  - 10000 itens  
- **Geração de dados**:  
  - Pesos e valores são inteiros aleatórios em [1,100) para cada instância  
  - **Capacidade da mochila**: 50 % da soma dos pesos  
- **Parâmetros padrão**:  
  - Iterações/Gerações = 100  
  - População/Agentes: GA=50, ACO=50, PSO=30, CS=25, Bee=30, Bat=30, Firefly=25, WOA=30

---

### 2. Metodologia

1. **Função de aptidão**  
   - Soma dos valores se o peso total ≤ capacidade; caso contrário, retorna 0 (penalização).

2. **Algoritmos testados**  
   - **Genetic Algorithm (GA)**: seleção por roleta, crossover de ponto único, mutação bit-flip.  
   - **Ant Colony Optimization (ACO)**: feromônio + heurística valor/peso, evaporação e depósito.  
   - **Particle Swarm Optimization (PSO)**: posições contínuas binarizadas via limiar 0.5.  
   - **Cuckoo Search (CS)**: vizinhança por “salto” simples e abandono de ninhos.  
   - **Bee Algorithm (BA)**: recrutamento ao redor de elites + exploradores aleatórios.  
   - **Bat Algorithm (Bat)**: posicionamento contínuo e binarização via função sigmoide.  
   - **Firefly Algorithm (Firefly)**: atração baseada em intensidade de luz e binarização.  
   - **Whale Optimization Algorithm (WOA)**: modelagem de encalhe e busca global/local.

3. **Configurações comuns**  
   - Número de iterações/gerações: **100**  
   - População/colônia/partículas conforme indicado acima  
   - Sementes aleatórias não fixas (resultados estocásticos)

4. **Dificuldade numérica: overflow na função sigmoide**  
   - Durante o **Bat Algorithm**, a binarização usa `prob = 1/(1+exp(-pos))`.  
   - Com `pos` muito grande, `exp(-pos)` estourava o limite numérico e gerava warnings de *overflow*.  
   - **Solução**: aplicamos  
     ```python
     z = np.clip(pos, -50, 50)
     prob = 1.0 / (1.0 + np.exp(-z))
     ```  
     limitando o argumento do exponencial a ±50, garantindo estabilidade sem alterar a dinâmica do algoritmo.

---

### 3. Resultados

#### 3.1. Instância com 1500 itens

| Algoritmo | Valor obtido | Tempo (s) |
|-----------|--------------|-----------|
| GA        | 39 264       | 1.8614    |
| ACO       | 48 282       | 4.8613    |
| PSO       | 39 283       | 0.5006    |
| Cuckoo    | 39 078       | 1.1397    |
| Bee       | 41 887       | 0.8703    |
| Bat       | 38 751       | 0.5429    |
| Firefly   | 38 975       | 0.8834    |
| WOA       | 39 316       | 0.4751    |

#### 3.2. Instância com 10000 itens

| Algoritmo | Valor obtido | Tempo (s) |
|-----------|--------------|-----------|
| GA        | 254 751      | 11.9178   |
| ACO       | 313 168      | 31.7903   |
| PSO       | 256 002      | 3.1107    |
| Cuckoo    | 251 826      | 7.2539    |
| Bee       | 256 291      | 5.6681    |
| Bat       | 252 285      | 3.3415    |
| Firefly   | 252 115      | 4.2189    |
| WOA       | 251 512      | 2.9787    |

---

### 4. Discussão

- **Qualidade da solução**  
  - ACO atingiu o **maior valor** (48 282 e 313 168), porém com maior custo computacional.  
  - Bee e PSO ficaram em níveis intermediários de valor, com PSO muito rápido.

- **Desempenho (tempo de execução)**  
  - **Mais rápido**: WOA (0.48 s e 2.98 s), seguido por PSO e Bat.  
  - **Mais lento**: ACO (4.86 s e 31.79 s).

- **Impacto do overflow**  
  - Sem o clipping, o Bat Algorithm gerava warnings e podia travar em instâncias grandes.  
  - Com o corte em ±50, o comportamento estatístico se manteve e as medidas de tempo e valor não foram afetadas.

---

### 5. Conclusão

- **ACO** é ideal para máxima qualidade, mas menos escalável em tempo.  
- **WOA** e **PSO** oferecem ótima relação valor/tempo para instâncias grandes.  
- O **Bat Algorithm** se beneficiou do tratamento de overflow, mantendo consistência sem penalizar desempenho.
