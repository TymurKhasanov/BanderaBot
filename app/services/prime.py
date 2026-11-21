import re
from datetime import datetime

from app.database.repository import SettingsRepository


DAY_NAMES = {
    "понеділок": 1,
    "вівторок": 2,
    "середа": 3,
    "четвер": 4,
    "п’ятниця": 5,
    "п'ятниця": 5,
    "субота": 6,
    "неділя": 7,
}

TIME_PATTERN = re.compile(r"\b(?:[01]\d|2[0-3]):[0-5]\d\b")


def parse_prime_schedule(text: str) -> list[tuple[int, str, str]]:
    schedule: list[tuple[int, str, str]] = []
    seen_days: set[int] = set()

    for raw_line in text.splitlines():
        line = " ".join(raw_line.split())
        lowered = line.casefold()
        day = next(
            (
                number
                for name, number in DAY_NAMES.items()
                if lowered.startswith(name)
            ),
            None,
        )
        if day is None:
            continue

        times = TIME_PATTERN.findall(line)
        if len(times) < 2:
            continue
        datetime.strptime(times[0], "%H:%M")
        datetime.strptime(times[1], "%H:%M")
        if day not in seen_days:
            schedule.append((day, times[0], times[1]))
            seen_days.add(day)

    return schedule


def save_prime_schedule(text: str) -> None:
    schedule = parse_prime_schedule(text)
    if not schedule:
        raise ValueError(
            "Не знайдено коректних рядків у форматі «Понеділок 20:00 - 21:00»."
        )
    SettingsRepository.replace_prime_schedule(text.strip(), schedule)
