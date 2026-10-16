# TaskAnalyzer

Projeto desenvolvido para a disciplina **Bootcamp III**, utilizando a abordagem
**Spec-Driven Development (SDD)** e práticas de governança de Inteligência
Artificial por meio de um **AI Harness**.

O TaskAnalyzer é um módulo Python responsável por analisar registros de tarefas
e gerar métricas relacionadas à conclusão, produtividade e cumprimento de prazos.

---

## Objetivo

O objetivo do projeto é implementar um analisador de tarefas orientado por uma
especificação formal, utilizando Inteligência Artificial como apoio à geração de
código, mas mantendo a especificação SDD e as regras de contexto como fontes de
verdade.

A implementação é validada por uma suíte automatizada de testes com `pytest`
e posteriormente submetida à revisão e homologação humana.

---

## Tecnologias

- Python 3.11+
- pytest
- Git
- GitHub
- Visual Studio Code

---

## Estrutura do Repositório

```text
sdd-task-analyzer/
│
├── specs/
│   └── task_analyzer_spec.md
│
├── src/
│   └── task_analyzer.py
│
├── tests/
│   └── test_harness.py
│
├── .gitignore
├── CONTEXT_RULES.md
├── README.md
└── requirements.txt
```

### Principais arquivos

- `specs/task_analyzer_spec.md`: contrato SDD utilizado como fonte de verdade
  para a implementação.
- `CONTEXT_RULES.md`: regras persistentes utilizadas para controlar o
  comportamento do assistente de IA.
- `src/task_analyzer.py`: implementação do módulo TaskAnalyzer.
- `tests/test_harness.py`: suíte de testes automatizados baseada nos cenários
  de aceite.
- `requirements.txt`: dependências autorizadas do projeto.

---

## Spec-Driven Development

O projeto utiliza **Spec-Driven Development (SDD)**.

Nesse modelo, a implementação deve ser derivada da especificação e não o
contrário.

O fluxo utilizado foi:

1. Definição da especificação SDD.
2. Definição das regras de governança da IA.
3. Criação dos cenários de aceite.
4. Implementação do Test Harness.
5. Geração e revisão do código com assistência de IA.
6. Execução dos testes automatizados.
7. Homologação humana.
8. Versionamento por meio de Git e GitHub.

---

## Governança de Inteligência Artificial

A implementação do TaskAnalyzer foi realizada com assistência de Inteligência
Artificial utilizando como fontes obrigatórias:

- `specs/task_analyzer_spec.md`
- `CONTEXT_RULES.md`

As regras de contexto impedem que o assistente altere o contrato público,
modifique os testes para favorecer a implementação ou introduza regras de
negócio que não estejam previstas na especificação.

O código gerado somente é considerado aprovado após a execução completa do
Test Harness e revisão humana.

---

## Funcionalidades

A função principal do projeto é:

```python
analyze_tasks(tasks)
```

Ela recebe uma lista de tarefas e retorna métricas consolidadas, incluindo:

- total de tarefas;
- total de tarefas concluídas;
- total de tarefas pendentes;
- tempo médio de conclusão;
- tempo médio de conclusão por prioridade;
- taxa percentual de atraso.

O módulo também possui a exceção customizada:

```python
TaskValidationError
```

utilizada para tratar violações das regras do contrato, como datas
cronologicamente inconsistentes.

---

## Regras principais

Para os cálculos temporais, somente tarefas com status `concluida` são
consideradas.

Uma tarefa é considerada atrasada somente quando:

```text
data_conclusao > data_prazo
```

Caso não existam tarefas concluídas, métricas que poderiam resultar em divisão
por zero retornam `0.0`.

Uma tarefa concluída deve possuir `data_conclusao`, e essa data não pode ser
anterior à `data_criacao`.

---

## Instalação

Clone o repositório e acesse sua pasta:

```bash
git clone <URL_DO_REPOSITORIO>
cd sdd-task-analyzer
```

Crie um ambiente virtual:

```powershell
py -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
py -m pip install -r requirements.txt
```

---

## Executando os Testes

Execute a suíte de testes com:

```powershell
py -m pytest -v
```

Resultado atual da Fase 2:

```text
6 passed
```

Todos os cenários automatizados atualmente definidos no Test Harness estão
sendo aprovados.

---

## Test Harness

A suíte localizada em:

```text
tests/test_harness.py
```

valida cenários como:

- cálculo correto das métricas;
- tempo médio geral;
- tempo médio por prioridade;
- taxa de atraso;
- data de conclusão anterior à criação;
- entrada vazia;
- conjunto contendo apenas tarefas pendentes;
- tarefa concluída sem data de conclusão;
- conclusão exatamente no prazo.

Os testes funcionam como critério objetivo de aceitação da implementação
gerada com assistência de IA.

---

## Homologação

Antes de considerar a implementação aprovada, são verificados:

- aderência ao contrato SDD;
- conformidade com `CONTEXT_RULES.md`;
- utilização de Python 3.11 ou superior;
- uso de type hints;
- tratamento específico de erros;
- prevenção de divisão por zero;
- legibilidade e organização do código;
- execução completa do Test Harness;
- revisão humana da implementação.

---

## Versionamento

O projeto utiliza branches de funcionalidade para separar as etapas de
desenvolvimento, incluindo:

```text
feature/sdd-specification
feature/test-harness
feature/task-analyzer-impl
```

As alterações são versionadas com commits descritivos e integradas à branch
`main` por meio de Pull Requests.

---

## Status do Projeto

**Fase 2 — Entrega Intermediária**

- Especificação SDD: concluída
- CONTEXT_RULES: concluído
- Test Harness: concluído
- Implementação TaskAnalyzer: concluída
- Testes automatizados: 100% aprovados
- Versionamento Git/GitHub: concluído