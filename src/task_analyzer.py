"""Analyze task completion metrics."""

import logging
from datetime import datetime
from typing import TypeAlias

logger = logging.getLogger(__name__)

TaskRecord: TypeAlias = dict[str, object]
AnalysisResult: TypeAlias = dict[str, int | float | dict[str, float]]

_PRIORITIES: tuple[str, ...] = ("Alta", "Média", "Baixa")
_REQUIRED_FIELDS: tuple[str, ...] = (
    "id",
    "titulo",
    "tipo",
    "prioridade",
    "data_criacao",
    "data_prazo",
    "status",
)


class TaskValidationError(ValueError):
    """Raised when a task does not satisfy the analyzer's validation rules."""


def _parse_datetime(value: object, field_name: str, task_id: object) -> datetime:
    """Parse a task date from a datetime or ISO-formatted string.

    Args:
        value: The date value to parse.
        field_name: The name of the field being parsed.
        task_id: The identifier of the task being validated.

    Returns:
        The parsed date and time.

    Raises:
        TaskValidationError: If the value is not a supported date or is invalid.
    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            parsed_value = datetime.fromisoformat(value)
        except ValueError as error:
            raise TaskValidationError(
                f"Tarefa {task_id!r}: '{field_name}' deve ser uma data ISO válida."
            ) from error
        if "T" not in value and " " not in value:
            raise TaskValidationError(
                f"Tarefa {task_id!r}: '{field_name}' deve incluir data e hora."
            )
        return parsed_value
    raise TaskValidationError(
        f"Tarefa {task_id!r}: '{field_name}' deve ser datetime ou string ISO."
    )


def _average(values: list[float]) -> float:
    """Return the arithmetic mean, or zero when no values are available.

    Args:
        values: The numeric values to average.

    Returns:
        The arithmetic mean or ``0.0`` for an empty list.
    """
    if not values:
        return 0.0
    return sum(values) / len(values)


def analyze_tasks(tasks: list[TaskRecord]) -> AnalysisResult:
    """Validate tasks and calculate completion and delay metrics.

    Args:
        tasks: Task records containing the fields defined by the SDD contract.

    Returns:
        A dictionary containing task totals, completion-time averages, and the
        percentage of completed tasks delivered after their deadlines.

    Raises:
        TaskValidationError: If the task collection or any task is invalid,
            including a completion date before its creation date.
    """
    if not isinstance(tasks, list):
        raise TaskValidationError("'tasks' deve ser uma lista de tarefas.")

    logger.info("Iniciando análise de %d tarefas.", len(tasks))

    total_completed = 0
    total_pending = 0
    completion_times: list[float] = []
    completion_times_by_priority: dict[str, list[float]] = {
        priority: [] for priority in _PRIORITIES
    }
    late_tasks = 0

    try:
        for index, task in enumerate(tasks):
            if not isinstance(task, dict):
                raise TaskValidationError(
                    f"Tarefa na posição {index} deve ser um dicionário."
                )

            task_id = task.get("id", f"posição {index}")
            if isinstance(task_id, bool) or not isinstance(task_id, (str, int)):
                raise TaskValidationError(
                    f"Tarefa na posição {index}: 'id' deve ser string ou inteiro."
                )

            missing_fields = [
                field for field in _REQUIRED_FIELDS if field not in task
            ]
            if missing_fields:
                raise TaskValidationError(
                    f"Tarefa {task_id!r}: campos obrigatórios ausentes: "
                    f"{', '.join(missing_fields)}."
                )

            for field_name in ("titulo", "tipo", "status"):
                if not isinstance(task[field_name], str):
                    raise TaskValidationError(
                        f"Tarefa {task_id!r}: '{field_name}' deve ser string."
                    )

            priority = task["prioridade"]
            if not isinstance(priority, str) or priority not in _PRIORITIES:
                raise TaskValidationError(
                    f"Tarefa {task_id!r}: 'prioridade' deve ser "
                    "Alta, Média ou Baixa."
                )

            created_at = _parse_datetime(
                task["data_criacao"], "data_criacao", task_id
            )
            deadline = _parse_datetime(task["data_prazo"], "data_prazo", task_id)
            status = task["status"]
            completed_at_value = task.get("data_conclusao")

            if completed_at_value is None:
                if status == "concluida":
                    raise TaskValidationError(
                        f"Tarefa {task_id!r}: 'data_conclusao' é obrigatória "
                        "para tarefas concluídas."
                    )
                if status == "pendente":
                    total_pending += 1
                continue

            completed_at = _parse_datetime(
                completed_at_value, "data_conclusao", task_id
            )
            try:
                if completed_at < created_at:
                    raise TaskValidationError(
                        f"Tarefa {task_id!r}: 'data_conclusao' não pode ser "
                        "anterior a 'data_criacao'."
                    )
                is_late = completed_at > deadline
            except TypeError as error:
                raise TaskValidationError(
                    f"Tarefa {task_id!r}: as datas devem usar formatos de fuso "
                    "horário compatíveis."
                ) from error

            if status == "pendente":
                total_pending += 1
            elif status == "concluida":
                duration_hours = (completed_at - created_at).total_seconds() / 3600
                completion_times.append(duration_hours)
                completion_times_by_priority[priority].append(duration_hours)
                total_completed += 1
                if is_late:
                    late_tasks += 1

    except TaskValidationError:
        logger.warning("Análise de tarefas interrompida por dados inválidos.")
        raise

    average_by_priority = {
        priority: _average(completion_times_by_priority[priority])
        for priority in _PRIORITIES
    }
    delay_rate = (
        (late_tasks / total_completed) * 100.0 if total_completed else 0.0
    )
    result: AnalysisResult = {
        "total_tarefas": len(tasks),
        "total_concluidas": total_completed,
        "total_pendentes": total_pending,
        "tempo_medio_conclusao_horas": _average(completion_times),
        "tempo_medio_por_prioridade_horas": average_by_priority,
        "taxa_atraso_percentual": delay_rate,
    }

    logger.info(
        "Análise concluída: %d concluídas, %d pendentes.",
        total_completed,
        total_pending,
    )
    return result
