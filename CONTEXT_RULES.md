# CONTEXT_RULES — TaskAnalyzer

## 1. Objetivo

Este arquivo define as regras persistentes de governança que deverão orientar qualquer assistente de Inteligência Artificial utilizado durante o desenvolvimento do projeto **TaskAnalyzer**.

O objetivo é garantir que o código gerado permaneça aderente:

- à especificação SDD definida em `specs/task_analyzer_spec.md`;
- às regras de negócio do projeto;
- às diretrizes arquiteturais;
- aos cenários de aceite;
- às restrições técnicas estabelecidas para a implementação.

O assistente de IA deverá considerar este arquivo e a especificação SDD como fontes obrigatórias de contexto antes de gerar ou modificar código.

---

## 2. Fonte de Verdade

A implementação deverá seguir rigorosamente os documentos:

- `CONTEXT_RULES.md`;
- `specs/task_analyzer_spec.md`.

O arquivo `specs/task_analyzer_spec.md` representa o contrato técnico e funcional do TaskAnalyzer.

O assistente de IA não deverá criar, alterar ou assumir comportamentos que não estejam explicitamente definidos na especificação.

---

## 3. Versão da Linguagem

O código deverá ser desenvolvido utilizando:

```text
Python 3.11 ou superior
```

Não deverão ser utilizadas funcionalidades incompatíveis com a versão mínima definida.

---

## 4. Tipagem

É obrigatório o uso de **type hints** em:

- funções;
- métodos;
- parâmetros;
- valores de retorno;
- assinaturas de classes, quando aplicável.

O código gerado deverá deixar explícitos os tipos esperados sempre que possível.

---

## 5. Padrões de Código

Todo código deverá seguir o padrão:

```text
PEP 8
```

A implementação deverá priorizar:

- legibilidade;
- clareza;
- organização;
- manutenibilidade;
- nomenclatura descritiva.

Nomes de funções, variáveis e classes deverão representar claramente sua responsabilidade dentro do domínio do TaskAnalyzer.

---

## 6. Princípio da Responsabilidade Única

A implementação deverá respeitar o princípio:

```text
Single Responsibility Principle — SRP
```

Cada função ou método deverá possuir um único propósito lógico.

Funções excessivamente grandes ou responsáveis por múltiplos comportamentos distintos deverão ser evitadas.

---

## 7. Coesão e Modularidade

As funções deverão ser:

- pequenas;
- coesas;
- independentes sempre que possível;
- organizadas de acordo com uma única responsabilidade de negócio.

O código deverá evitar acoplamento desnecessário entre componentes.

---

## 8. Documentação do Código

Todos os módulos, classes e funções deverão possuir documentação adequada.

As docstrings deverão seguir o padrão:

```text
Google Style Docstrings
```

A documentação deverá deixar claro:

- o propósito da função;
- os parâmetros recebidos;
- o valor retornado;
- as exceções relevantes, quando aplicável.

---

## 9. Tratamento de Exceções

O sistema deverá utilizar tratamento específico de exceções.

Devem ser evitados blocos genéricos como:

```python
except Exception:
    pass
```

Sempre que existir uma exceção específica adequada, ela deverá ser utilizada.

Erros deverão possuir mensagens claras e descritivas.

As validações de negócio relacionadas às tarefas deverão utilizar a exceção customizada definida na especificação:

```python
TaskValidationError
```

---

## 10. Prevenção de Divisão por Zero

A implementação deverá tratar preventivamente situações em que não existam dados válidos para cálculo de médias ou taxas.

Quando a especificação determinar ausência de dados válidos, deverão ser retornados valores zerados padronizados:

```python
0.0
```

Não deverão ocorrer exceções não tratadas por divisão por zero.

---

## 11. Logs

A rastreabilidade da aplicação deverá utilizar a biblioteca padrão:

```python
logging
```

Os logs deverão ser utilizados para registrar, quando aplicável:

- fluxo de execução;
- validações importantes;
- métricas principais;
- erros identificados.

Não deverão ser adicionadas bibliotecas externas de logging sem autorização explícita.

---

## 12. Dependências

Bibliotecas externas somente poderão ser utilizadas quando estiverem explicitamente autorizadas no escopo do projeto.

Para a Fase 2, a dependência externa prevista para o Test Harness é:

```text
pytest
```

Bibliotecas adicionais não deverão ser introduzidas sem alteração formal da especificação ou autorização correspondente.

---

## 13. Imutabilidade do Contrato

O assistente de IA não poderá alterar:

- o nome das funções públicas;
- os parâmetros das funções públicas;
- a estrutura de entrada;
- a estrutura de saída;
- os cenários de aceite;
- as regras de negócio;
- a estrutura de diretórios definida para o projeto;

sem atualização formal prévia da especificação SDD.

A função pública definida para a Fase 2 é:

```python
analyze_tasks(tasks)
```

---

## 14. Testes

Os cenários de teste definidos no planejamento e na especificação não deverão ser:

- removidos;
- alterados;
- enfraquecidos;
- adaptados apenas para fazer o código passar.

Os testes deverão validar o comportamento esperado da implementação.

A suíte de testes deverá utilizar:

```text
pytest
```

e residir em:

```text
tests/test_harness.py
```

---

## 15. Critério de Aprovação

Nenhum código gerado ou modificado por um assistente de IA deverá ser considerado aprovado para integração na branch principal sem que:

1. a implementação esteja aderente ao contrato SDD;
2. estas regras de contexto tenham sido respeitadas;
3. o Test Harness tenha sido executado;
4. 100% dos testes tenham sido aprovados;
5. a implementação tenha passado por revisão humana.

---

## 16. Proibições Explícitas

O assistente de IA não deverá:

### 16.1 Utilizar bibliotecas não autorizadas

Não utilizar bibliotecas externas que não estejam explicitamente autorizadas no projeto.

### 16.2 Alterar os testes para adequá-los ao código

Os testes deverão representar o contrato.

O código deverá ser corrigido para atender aos testes e à especificação, e não o contrário.

### 16.3 Alterar a estrutura do repositório

A estrutura de pastas e arquivos definida no projeto não deverá ser modificada sem autorização prévia.

### 16.4 Implementar persistência

Não implementar lógica de persistência em:

- arquivos locais;
- bancos de dados;
- serviços externos.

Persistência não faz parte do escopo definido para esta fase.

### 16.5 Alterar assinaturas públicas

Os nomes e parâmetros das funções públicas descritas na especificação não deverão ser alterados.

### 16.6 Criar funcionalidade sem teste correspondente

Nenhuma nova funcionalidade deverá ser adicionada sem que exista uma validação correspondente no Test Harness.

### 16.7 Produzir código duplicado

Não inserir código:

- duplicado;
- redundante;
- sem necessidade arquitetural.

### 16.8 Inventar regras de negócio

O assistente não deverá assumir comportamentos, regras ou lógicas que não estejam explicitamente descritos no contrato SDD.

Quando uma regra não estiver definida na especificação, ela não deverá ser criada automaticamente.

---

## 17. Relação com o SDD

O desenvolvimento deverá seguir o fluxo:

```text
Especificação SDD
        ↓
CONTEXT_RULES
        ↓
Test Harness
        ↓
Implementação
        ↓
Execução dos testes
        ↓
Homologação humana
```

A IA atua como ferramenta de implementação.

A especificação SDD permanece como contrato que define o comportamento esperado do sistema.

---

## 18. Homologação Humana

Antes da integração do código à branch principal, deverá ser realizada revisão humana contemplando:

- aderência ao `task_analyzer_spec.md`;
- aderência ao `CONTEXT_RULES.md`;
- legibilidade do código;
- uso adequado de type hints;
- tratamento de exceções;
- conformidade com PEP 8;
- cumprimento das proibições explícitas;
- resultado do Test Harness.

Somente após essa validação o código poderá ser considerado homologado.