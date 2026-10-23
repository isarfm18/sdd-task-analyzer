"""Acceptance tests for the TaskAnalyzer SDD contract."""

import pytest

from src.task_analyzer import TaskValidationError, analyze_tasks


def _task(
    task_id: int,
    priority: str,
    created_at: str,
    deadline: str,
    status: str,
    completed_at: str | None = None,
) -> dict[str, object]:
    """Build a task record for acceptance tests.

    Args:
        task_id: Unique task identifier.
        priority: Task priority.
        created_at: Creation date and time in ISO format.
        deadline: Deadline in ISO format.
        status: Task status.
        completed_at: Optional completion date and time in ISO format.

    Returns:
        A task record matching the analyzer input contract.
    """
    return {
        "id": task_id,
        "titulo": f"Tarefa {task_id}",
        "tipo": "Desenvolvimento",
        "prioridade": priority,
        "data_criacao": created_at,
        "data_prazo": deadline,
        "data_conclusao": completed_at,
        "status": status,
    }


def test_analyze_tasks_returns_expected_metrics() -> None:
    """Calculate totals, completion averages, and delay percentage."""
    tasks = [
        _task(
            1,
            "Alta",
            "2025-01-01T09:00:00",
            "2025-01-01T12:00:00",
            "concluida",
            "2025-01-01T11:00:00",
        ),
        _task(
            2,
            "Baixa",
            "2025-01-02T09:00:00",
            "2025-01-02T11:00:00",
            "concluida",
            "2025-01-02T13:00:00",
        ),
        _task(
            3,
            "Média",
            "2025-01-03T09:00:00",
            "2025-01-04T09:00:00",
            "pendente",
        ),
        _task(
            4,
            "Alta",
            "2025-01-04T09:00:00",
            "2025-01-05T09:00:00",
            "cancelada",
        ),
    ]

    result = analyze_tasks(tasks)

    assert result == {
        "total_tarefas": 4,
        "total_concluidas": 2,
        "total_pendentes": 1,
        "tempo_medio_conclusao_horas": 3.0,
        "tempo_medio_por_prioridade_horas": {
            "Alta": 2.0,
            "Média": 0.0,
            "Baixa": 4.0,
        },
        "taxa_atraso_percentual": 50.0,
    }


def test_analyze_tasks_rejects_completion_before_creation() -> None:
    """Raise TaskValidationError for chronologically inconsistent dates."""
    task = _task(
        1,
        "Alta",
        "2025-01-01T10:00:00",
        "2025-01-01T12:00:00",
        "concluida",
        "2025-01-01T09:00:00",
    )

    with pytest.raises(TaskValidationError, match="anterior"):
        analyze_tasks([task])


def test_analyze_tasks_returns_zero_metrics_for_empty_input() -> None:
    """Return zero totals and metrics when there are no tasks."""
    result = analyze_tasks([])

    assert result == {
        "total_tarefas": 0,
        "total_concluidas": 0,
        "total_pendentes": 0,
        "tempo_medio_conclusao_horas": 0.0,
        "tempo_medio_por_prioridade_horas": {
            "Alta": 0.0,
            "Média": 0.0,
            "Baixa": 0.0,
        },
        "taxa_atraso_percentual": 0.0,
    }


def test_analyze_tasks_returns_zero_completion_metrics_for_pending_tasks() -> None:
    """Exclude pending tasks from completion metrics without dividing by zero."""
    tasks = [
        _task(
            1,
            "Alta",
            "2025-01-01T09:00:00",
            "2025-01-02T09:00:00",
            "pendente",
        ),
        _task(
            2,
            "Baixa",
            "2025-01-03T09:00:00",
            "2025-01-04T09:00:00",
            "pendente",
        ),
    ]

    result = analyze_tasks(tasks)

    assert result == {
        "total_tarefas": 2,
        "total_concluidas": 0,
        "total_pendentes": 2,
        "tempo_medio_conclusao_horas": 0.0,
        "tempo_medio_por_prioridade_horas": {
            "Alta": 0.0,
            "Média": 0.0,
            "Baixa": 0.0,
        },
        "taxa_atraso_percentual": 0.0,
    }

def test_analyze_tasks_rejects_completed_task_without_completion_date() -> None:
    """Raise TaskValidationError when a completed task has no completion date."""
    task = _task(
        1,
        "Alta",
        "2025-01-01T09:00:00",
        "2025-01-02T09:00:00",
        "concluida",
    )

    with pytest.raises(TaskValidationError):
        analyze_tasks([task])


def test_analyze_tasks_does_not_mark_deadline_completion_as_delayed() -> None:
    """Do not count a task completed exactly at the deadline as delayed."""
    task = _task(
        1,
        "Alta",
        "2025-01-01T09:00:00",
        "2025-01-01T12:00:00",
        "concluida",
        "2025-01-01T12:00:00",
    )

    result = analyze_tasks([task])

    assert result["taxa_atraso_percentual"] == 0.0


def test_fusos_horarios_incompativeis():
    """Verifica o tratamento de datas com fusos incompatíveis."""
    tarefa = {
        "id": 100,
        "titulo": "Teste de fuso horário",
        "tipo": "Desenvolvimento",
        "prioridade": "Alta",
        "data_criacao": "2026-10-20T09:00:00",
        "data_prazo": "2026-10-20T18:00:00+00:00",
        "data_conclusao": "2026-10-20T15:00:00+00:00",
        "status": "concluida",
    }

    with pytest.raises(TaskValidationError, match="fuso"):
        analyze_tasks([tarefa])
