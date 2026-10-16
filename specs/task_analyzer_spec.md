# TaskAnalyzer — Especificação SDD

## 1. Identificação

**Projeto:** TaskAnalyzer  
**Disciplina:** Bootcamp III  
**Documento:** Especificação SDD do TaskAnalyzer  
**Origem:** Especificação elaborada na Fase 1 — Entrega Inicial  
**Aplicação:** Fase 2 — Entrega Intermediária  

---

## 2. Objetivo

O TaskAnalyzer é um módulo de inteligência analítica voltado ao processamento de métricas de produtividade relacionadas a tarefas.

O sistema deve analisar registros de tarefas, calcular métricas de tempo de conclusão, identificar atrasos, gerar indicadores segmentados por prioridade e disponibilizar informações estruturadas para apoio à tomada de decisão.

A implementação deverá seguir o paradigma de **Spec-Driven Development (SDD)**, utilizando este documento como contrato técnico para orientar:

- a geração do código-fonte;
- a implementação do Test Harness;
- a validação automatizada;
- a homologação humana da solução.

---

## 3. Contrato de Interface

### 3.1 Função pública

O módulo deverá disponibilizar a seguinte função pública:

```python
analyze_tasks(tasks)
```

A função será responsável por receber uma coleção de tarefas, validar os dados conforme as regras deste contrato, calcular as métricas previstas e retornar os resultados em uma estrutura organizada.

A implementação deverá utilizar **type hints**.

A assinatura pública da função não poderá ser alterada por assistentes de Inteligência Artificial sem atualização formal prévia deste contrato.

---

## 4. Estrutura de Entrada

A função `analyze_tasks` deverá receber uma lista de registros de tarefas.

Cada tarefa deverá possuir os seguintes campos:

### 4.1 `id`

**Tipo esperado:** `str` ou `int`

Identificador único da tarefa.

### 4.2 `titulo`

**Tipo esperado:** `str`

Nome ou descrição resumida da tarefa.

### 4.3 `tipo`

**Tipo esperado:** `str`

Categoria ou classificação operacional da tarefa.

Exemplos:

- Desenvolvimento
- Correção
- Revisão

### 4.4 `prioridade`

**Tipo esperado:** `str`

Valores permitidos:

- Alta
- Média
- Baixa

### 4.5 `data_criacao`

**Tipo esperado:** `datetime` ou string representando data e hora.

Representa a data e a hora em que a tarefa foi criada.

### 4.6 `data_prazo`

**Tipo esperado:** `datetime` ou string representando data e hora.

Representa a data e a hora limite prevista para conclusão da tarefa.

### 4.7 `data_conclusao`

**Tipo esperado:** `datetime`, string representando data e hora ou `None`.

Representa a data e a hora em que a tarefa foi efetivamente concluída.

Para tarefas que ainda não tenham sido concluídas, o campo poderá conter `None` ou estar ausente.

Para tarefas consideradas concluídas, a data de conclusão deverá estar preenchida.

### 4.8 `status`

**Tipo esperado:** `str`

Representa o estado atual da tarefa.

Exemplos previstos no contrato:

- `concluida`
- `pendente`
- `cancelada`

---

## 5. Estrutura de Saída

A função deverá retornar um objeto estruturado, representado em Python por um dicionário.

Para a Fase 2, o retorno deverá contemplar, no mínimo, as métricas descritas a seguir.

### 5.1 `total_tarefas`

Quantidade total de tarefas recebidas para processamento.

**Tipo esperado:** `int`

### 5.2 `total_concluidas`

Quantidade de tarefas consideradas concluídas.

**Tipo esperado:** `int`

### 5.3 `total_pendentes`

Quantidade de tarefas consideradas pendentes.

**Tipo esperado:** `int`

### 5.4 `tempo_medio_conclusao_horas`

Tempo médio de conclusão das tarefas concluídas, considerando a diferença entre `data_criacao` e `data_conclusao`.

**Tipo esperado:** `float`

A unidade utilizada deverá ser **horas**.

Quando não existirem tarefas concluídas válidas para o cálculo, deverá ser retornado:

```python
0.0
```

### 5.5 `tempo_medio_por_prioridade_horas`

Tempo médio de conclusão segmentado por nível de prioridade.

**Tipo esperado:** `dict`

Deverão ser consideradas as categorias:

- Alta
- Média
- Baixa

Cada valor deverá representar o tempo médio de conclusão, em horas, das tarefas concluídas pertencentes à respectiva prioridade.

Quando não houver tarefas concluídas para determinada prioridade, o valor correspondente deverá ser:

```python
0.0
```

> **Observação:** o nome `tempo_medio_por_prioridade_horas` foi adotado nesta transposição para formalizar a métrica por prioridade exigida na Fase 2.

### 5.6 `taxa_atraso_percentual`

Percentual de tarefas concluídas cuja data de conclusão ultrapasse a data limite prevista.

Uma tarefa será considerada atrasada quando:

```text
data_conclusao > data_prazo
```

**Tipo esperado:** `float`

Quando não existirem tarefas concluídas válidas para o cálculo, deverá ser retornado:

```python
0.0
```

---

## 6. Requisitos Funcionais

### RF01 — Recepção de Dados

O sistema deve receber um conjunto de registros de tarefas.

### RF02 — Estrutura Mínima da Tarefa

Cada tarefa deverá fornecer os dados necessários para identificação, classificação, prioridade, controle temporal e situação atual.

### RF03 — Validação da Data de Conclusão

Para tarefas consideradas concluídas, a data de conclusão deverá estar preenchida.

### RF04 — Filtro de Tarefas Efetivadas

As métricas temporais devem considerar exclusivamente tarefas concluídas.

Tarefas pendentes ou canceladas não devem participar do cálculo do tempo médio de conclusão.

### RF05 — Validação Cronológica

O sistema deverá verificar a coerência das datas.

A data de conclusão não poderá ser anterior à data de criação.

### RF06 — Tempo Médio Geral

O sistema deverá calcular o tempo médio de conclusão das tarefas concluídas.

### RF07 — Tempo Médio por Prioridade

O sistema deverá segmentar o cálculo do tempo médio de conclusão por nível de prioridade.

### RF08 — Taxa de Atraso Global

O sistema deverá calcular a porcentagem de tarefas concluídas depois do prazo estabelecido.

### RF09 — Relatório Estruturado

O resultado deverá ser retornado em uma estrutura organizada, como um dicionário Python, permitindo sua utilização por outros componentes.

---

## 7. Regras de Negócio

### RN01 — Critério de Inclusão Temporal

Somente tarefas concluídas devem participar dos cálculos de métricas temporais.

Tarefas pendentes ou canceladas deverão ser desconsideradas nesses cálculos.

### RN02 — Validação de Consistência Cronológica

A data e a hora de conclusão de uma tarefa nunca poderão ser anteriores à data e à hora de criação.

A seguinte condição é inválida:

```text
data_conclusao < data_criacao
```

Quando essa inconsistência for identificada, o sistema deverá rejeitar o registro utilizando a exceção customizada:

```python
TaskValidationError
```

### RN03 — Prevenção de Divisão por Zero

Quando não existirem tarefas concluídas disponíveis para o cálculo de uma média ou taxa proporcional, o sistema deverá retornar:

```python
0.0
```

O sistema não deverá gerar exceções não tratadas decorrentes de divisão por zero.

### RN04 — Segmentação das Métricas

O tempo médio de conclusão deverá ser disponibilizado de forma geral e também segmentado por nível de prioridade.

As prioridades previstas são:

- Alta
- Média
- Baixa

### RN05 — Apuração de Atrasos

Uma tarefa deverá ser considerada entregue com atraso quando:

```text
data_conclusao > data_prazo
```

### RN06 — Imutabilidade do Contrato

A assinatura da função pública, a estrutura de entrada, a estrutura de saída e as regras de negócio definidas neste documento não deverão ser modificadas por assistentes de Inteligência Artificial sem atualização formal prévia da especificação SDD.

---

## 8. Tratamento de Erros

### 8.1 `TaskValidationError`

A implementação deverá disponibilizar uma exceção customizada denominada:

```python
TaskValidationError
```

Essa exceção deverá representar violações das regras de validação de negócio do TaskAnalyzer.

Ela deverá ser disparada, no mínimo, quando uma tarefa apresentar:

```text
data_conclusao < data_criacao
```

A mensagem da exceção deverá ser clara e descrever a inconsistência encontrada.

O tratamento não deverá utilizar capturas genéricas de exceção quando existir uma exceção específica adequada.

---

## 9. Cenários de Aceite

### 9.1 Cenário 1 — Sucesso: cálculo correto das métricas

**Dado** um conjunto de tarefas válidas contendo diferentes prioridades, datas de criação consistentes, datas de conclusão válidas e diferentes situações,

**Quando** a função `analyze_tasks` processar esse conjunto,

**Então** o sistema deverá retornar corretamente:

- total de tarefas;
- total de tarefas concluídas;
- total de tarefas pendentes;
- tempo médio geral de conclusão em horas;
- tempo médio de conclusão por prioridade;
- taxa percentual de atraso.

### 9.2 Cenário 2 — Exceção: datas inválidas

**Dado** um conjunto contendo uma tarefa cuja data de conclusão seja anterior à data de criação,

**Quando** `analyze_tasks` tentar processar essa tarefa,

**Então** o sistema deverá interromper o processamento inválido por meio da exceção:

```python
TaskValidationError
```

A exceção deverá possuir uma mensagem clara e descritiva.

### 9.3 Cenário 3 — Prevenção de divisão por zero

**Dado** um conjunto de dados que não contenha tarefas concluídas,

**Quando** o TaskAnalyzer tentar calcular médias ou taxas dependentes de tarefas concluídas,

**Então** deverá retornar:

```python
0.0
```

para essas métricas, sem lançar exceções não tratadas.

### 9.4 Caso de borda — Entrada vazia

**Dado** uma lista de tarefas vazia,

**Quando** `analyze_tasks` for executada,

**Então** o sistema deverá retornar totais zerados e valores `0.0` para as métricas que dependem de tarefas concluídas, sem provocar falha de execução.

### 9.5 Caso de borda — Apenas tarefas pendentes

**Dado** um conjunto formado apenas por tarefas pendentes,

**Quando** `analyze_tasks` for executada,

**Então**:

- `total_tarefas` deverá refletir a quantidade recebida;
- `total_concluidas` deverá ser igual a zero;
- `total_pendentes` deverá refletir a quantidade de tarefas pendentes;
- as métricas temporais sem dados concluídos deverão retornar `0.0`;
- nenhuma exceção de divisão por zero deverá ocorrer.

---

## 10. Test Harness

Os cenários definidos nesta especificação deverão ser traduzidos em testes automatizados utilizando o framework `pytest`.

Os testes deverão residir em:

```text
tests/test_harness.py
```

A suíte deverá validar, no mínimo:

1. processamento correto de tarefas válidas;
2. cálculo dos totais;
3. cálculo do tempo médio geral;
4. cálculo do tempo médio por prioridade;
5. cálculo da taxa de atraso;
6. tratamento de datas cronologicamente inválidas;
7. entrada vazia;
8. conjunto contendo apenas tarefas pendentes.

Nenhum código gerado por Inteligência Artificial deverá ser considerado homologado enquanto a suíte de testes não atingir **100% de aprovação**.

Comando previsto:

```bash
pytest -v
```

---

## 11. Requisitos Não Funcionais Aplicáveis

A implementação deverá:

- utilizar Python 3.11 ou superior;
- utilizar type hints em funções, parâmetros e retornos;
- seguir o padrão PEP 8;
- respeitar o Princípio da Responsabilidade Única (SRP);
- utilizar Google Style Docstrings;
- utilizar tratamento específico de exceções;
- utilizar a biblioteca padrão `logging` para rastreabilidade;
- utilizar `pytest` para automação dos testes;
- respeitar integralmente as regras estabelecidas em `CONTEXT_RULES.md`.

---

## 12. Restrições

A implementação não deverá:

- alterar os cenários de aceite definidos neste contrato;
- modificar a assinatura da função pública sem atualização formal do SDD;
- utilizar bibliotecas externas não autorizadas;
- implementar persistência em arquivos ou banco de dados;
- adicionar funcionalidades que não estejam previstas neste contrato;
- adicionar código duplicado ou sem necessidade arquitetural;
- assumir regras de negócio não documentadas.

---

## 13. Critério de Homologação

A implementação somente poderá ser considerada aprovada após:

1. execução completa do Test Harness;
2. aprovação de 100% dos testes;
3. comparação do código com esta especificação;
4. comparação do código com `CONTEXT_RULES.md`;
5. revisão dos type hints;
6. revisão do tratamento de exceções;
7. verificação das restrições arquiteturais;
8. homologação humana antes da integração à branch `main`.

---

## 14. Rastreabilidade da Especificação

Este arquivo é uma transposição operacional da Especificação SDD elaborada na Fase 1 do projeto TaskAnalyzer.

Foram preservados da Fase 1:

- objetivo do sistema;
- estrutura das tarefas;
- regras de validação;
- cálculo de métricas temporais;
- segmentação por prioridade;
- regra de atraso;
- prevenção de divisão por zero;
- cenários de aceite;
- requisitos arquiteturais;
- critérios de homologação.

Para atender aos requisitos explícitos da Fase 2, foram formalizados também:

- a função pública `analyze_tasks`;
- a exceção customizada `TaskValidationError`;
- `total_tarefas`;
- `total_concluidas`;
- `total_pendentes`;
- o nome das métricas utilizadas pelo Test Harness;
- os casos de borda de entrada vazia e tarefas apenas pendentes.

Qualquer alteração futura neste contrato deverá ser realizada de forma explícita e versionada antes da alteração correspondente no código-fonte.