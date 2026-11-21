import unittest
from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardButton

from app.keyboards.dcp_rosters import rosters_keyboard
from app.handlers.dcp import (
    filtered_rosters,
    roster_detail_text,
    roster_list_text,
)
from app.services.prime import parse_prime_schedule
from app.scheduler.jobs import get_due_prime


class PrimeScheduleTests(unittest.TestCase):
    def test_parses_supported_days_and_valid_times(self) -> None:
        schedule = parse_prime_schedule(
            "Понеділок 20:00 - 21:30\n"
            "Неділя: 18:15-19:00\n"
            "невідомий рядок"
        )
        self.assertEqual(
            schedule,
            [(1, "20:00", "21:30"), (7, "18:15", "19:00")],
        )

    def test_ignores_invalid_times(self) -> None:
        schedule = parse_prime_schedule("Вівторок 24:00 - 26:00")
        self.assertEqual(schedule, [])

    def test_does_not_add_same_day_twice(self) -> None:
        schedule = parse_prime_schedule(
            "Середа 19:00 - 20:00\nСереда 21:00 - 22:00"
        )
        self.assertEqual(schedule, [(3, "19:00", "20:00")])


class RosterKeyboardTests(unittest.TestCase):
    def test_uses_string_callback_data(self) -> None:
        keyboard = rosters_keyboard([{"id": 12, "name": "Main"}])
        button = keyboard.inline_keyboard[0][0]
        self.assertIsInstance(button, InlineKeyboardButton)
        self.assertEqual(button.callback_data, "roster:12")

    def test_rejects_missing_id(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing id"):
            rosters_keyboard([{"name": "Broken"}])

    def test_rejects_long_callback_data(self) -> None:
        with self.assertRaisesRegex(ValueError, "64 bytes"):
            rosters_keyboard(
                [{"id": "x" * 64, "name": "Too long"}],
                prefix="roster",
            )


class RosterPresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rosters = [
            {
                "id": "roster-1",
                "name": "Alpha",
                "packKind": "PHYS",
                "gradeApproved": False,
                "coefficient": 1,
                "screenshotRequired": False,
                "balances": {
                    "normal": {"available": 10, "reserved": 0},
                    "epic": {"available": 30, "reserved": 0},
                },
                "members": [
                    {
                        "nickname": "Archer",
                        "className": "HAWKEYE",
                        "level": 68,
                        "grade": "A",
                    },
                    {
                        "nickname": "Healer",
                        "className": "BISHOP",
                        "level": 66,
                        "grade": "B",
                    },
                ],
            },
            {
                "id": "roster-2",
                "name": "Beta",
                "packKind": "MAG",
                "balances": {
                    "normal": {"available": 20, "reserved": 0},
                    "epic": {"available": 5, "reserved": 0},
                },
                "members": [
                    {
                        "nickname": "Mage",
                        "className": "SORCERER",
                        "level": 70,
                        "grade": "A",
                    }
                ],
            },
        ]

    def test_filters_and_sorts_rosters_by_balance(self) -> None:
        result = filtered_rosters(self.rosters, "normal", "all")
        self.assertEqual([roster["name"] for roster in result], ["Beta", "Alpha"])
        self.assertEqual(
            [roster["name"] for roster in filtered_rosters(
                self.rosters,
                "name",
                "mag",
            )],
            ["Beta"],
        )

    def test_list_contains_compact_roster_metrics(self) -> None:
        text = roster_list_text(self.rosters, "name", "all")
        self.assertIn("Lv 67.0", text)
        self.assertIn("💵 10 · 💎 30", text)

    def test_detail_groups_members_by_role(self) -> None:
        text = roster_detail_text(self.rosters[0])
        self.assertIn("🏹 DD", text)
        self.assertIn("❤️ Хіл", text)
        self.assertIn("Archer</b> — Hawkeye · Lv 68 · A", text)


class PrimeReminderTests(unittest.TestCase):
    def test_finds_midnight_prime_from_previous_day(self) -> None:
        kyiv = ZoneInfo("Europe/Kyiv")
        now = datetime(2026, 11, 21, 23, 45, tzinfo=kyiv)

        def schedule(day: int):
            if day == 7:
                return {"start_time": "00:15", "end_time": "01:00"}
            return None

        with patch(
            "app.scheduler.jobs.SettingsRepository.get_today_prime",
            side_effect=schedule,
        ):
            prime_date, prime = get_due_prime(now)

        self.assertEqual(prime_date.isoformat(), "2026-11-22")
        self.assertEqual(prime["start_time"], "00:15")


if __name__ == "__main__":
    unittest.main()
