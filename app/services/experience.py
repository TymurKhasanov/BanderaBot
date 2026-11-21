import json
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR
from functools import lru_cache
from pathlib import Path


EXP_TABLE_FILE = Path(__file__).resolve().parents[1] / "data" / "exp_table.json"
MIN_LEVEL = 1
MAX_LEVEL = 75


@lru_cache(maxsize=1)
def load_exp_table() -> dict[int, dict[str, int]]:
    with EXP_TABLE_FILE.open("r", encoding="utf-8") as file:
        raw = json.load(file)
    return {
        int(level): {
            "total": int(values["total"]),
            "to_level": int(values["to_level"]),
        }
        for level, values in raw.items()
    }


def parse_level(value: str) -> int:
    try:
        level = int(value.strip())
    except ValueError as exc:
        raise ValueError("Вкажіть рівень цілим числом, наприклад 68.") from exc
    if level < MIN_LEVEL or level >= MAX_LEVEL:
        raise ValueError(
            f"Для розрахунку доступні рівні від {MIN_LEVEL} до {MAX_LEVEL - 1}."
        )
    return level


def parse_percent(value: str) -> Decimal:
    normalized = value.strip().replace(",", ".").rstrip("%").strip()
    try:
        percent = Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError("Вкажіть процент числом, наприклад 53,5.") from exc
    if percent < 0 or percent > 100:
        raise ValueError("Процент має бути від 0 до 100.")
    return percent


def calculate_remaining_exp(level: int, percent: Decimal) -> dict[str, int]:
    table = load_exp_table()
    next_level = level + 1
    next_row = table.get(next_level)
    if next_row is None:
        raise ValueError(f"Для рівня {next_level} немає даних у таблиці.")

    required = Decimal(next_row["to_level"])
    earned = (required * percent / Decimal(100)).to_integral_value(
        rounding=ROUND_FLOOR
    )
    remaining = required - earned
    return {
        "current_level": level,
        "next_level": next_level,
        "required": int(required),
        "earned": int(earned),
        "remaining": max(0, int(remaining.to_integral_value(rounding=ROUND_CEILING))),
    }


def format_exp(value: int) -> str:
    return f"{value:,}".replace(",", " ")
