"""Core parser, validator, explainer, builder and preview engine for five-field cron."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

FIELD_SPECS = (
    ("minute", 0, 59),
    ("hour", 0, 23),
    ("day of month", 1, 31),
    ("month", 1, 12),
    ("day of week", 0, 7),
)
MONTH_NAMES = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}
DOW_NAMES = {"SUN":0,"MON":1,"TUE":2,"WED":3,"THU":4,"FRI":5,"SAT":6}

class CronError(ValueError):
    """Raised for invalid cron input."""

@dataclass(frozen=True)
class CronExpression:
    minute: str
    hour: str
    day: str
    month: str
    weekday: str

    @classmethod
    def parse(cls, expression: str) -> "CronExpression":
        parts = expression.split()
        if len(parts) != 5:
            raise CronError("Expected exactly 5 fields: minute hour day-of-month month day-of-week")
        obj = cls(*parts)
        obj.validate()
        return obj

    def validate(self) -> None:
        for value, spec in zip(self.fields, FIELD_SPECS):
            _parse_field(value, spec[1], spec[2], spec[0])

    @property
    def fields(self) -> tuple[str, ...]:
        return (self.minute, self.hour, self.day, self.month, self.weekday)

    def __str__(self) -> str:
        return " ".join(self.fields)

    def matches(self, dt: datetime) -> bool:
        values = (dt.minute, dt.hour, dt.day, dt.month, (dt.weekday() + 1) % 7)
        sets = [_parse_field(v, spec[1], spec[2], spec[0]) for v, spec in zip(self.fields, FIELD_SPECS)]
        dom_match = values[2] in sets[2]
        dow_match = values[4] in {0 if x == 7 else x for x in sets[4]}
        # Vixie cron semantics: when both DOM and DOW are restricted, either may match.
        day_ok = (dom_match or dow_match) if self.day != "*" and self.weekday != "*" else (dom_match and dow_match)
        return values[0] in sets[0] and values[1] in sets[1] and day_ok and values[3] in sets[3]

    def next_runs(self, start: datetime, count: int = 5, max_minutes: int = 5_256_000) -> list[datetime]:
        if count < 1 or count > 100:
            raise CronError("count must be between 1 and 100")
        cursor = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
        out: list[datetime] = []
        for _ in range(max_minutes):
            if self.matches(cursor):
                out.append(cursor)
                if len(out) == count:
                    return out
            cursor += timedelta(minutes=1)
        raise CronError("No matching run found within preview horizon")

    def explain(self) -> str:
        common = {
            "* * * * *": "Every minute",
            "0 * * * *": "At minute 0 of every hour",
            "0 0 * * *": "Every day at 00:00",
            "0 0 * * 0": "Every Sunday at 00:00",
            "0 0 1 * *": "At 00:00 on day 1 of every month",
        }
        if str(self) in common:
            return common[str(self)]
        return "; ".join(_describe(v, spec[0]) for v, spec in zip(self.fields, FIELD_SPECS))

def build(minute="*", hour="*", day="*", month="*", weekday="*") -> CronExpression:
    return CronExpression.parse(f"{minute} {hour} {day} {month} {weekday}")

def _atom(value: str, minimum: int, maximum: int, field: str) -> int:
    names = MONTH_NAMES if field == "month" else DOW_NAMES if field == "day of week" else {}
    upper = value.upper()
    if upper in names:
        return names[upper]
    try:
        number = int(value)
    except ValueError as exc:
        raise CronError(f"Invalid {field} value: {value}") from exc
    if not minimum <= number <= maximum:
        raise CronError(f"{field} value {number} is outside {minimum}-{maximum}")
    return number

def _parse_field(text: str, minimum: int, maximum: int, field: str) -> set[int]:
    if not text or any(c.isspace() for c in text):
        raise CronError(f"Invalid {field} field")
    result: set[int] = set()
    for item in text.split(","):
        base, slash, step_text = item.partition("/")
        step = 1
        if slash:
            try: step = int(step_text)
            except ValueError as exc: raise CronError(f"Invalid {field} step: {step_text}") from exc
            if step < 1: raise CronError(f"{field} step must be positive")
        if base == "*":
            start, end = minimum, maximum
        elif "-" in base:
            left, right = base.split("-", 1)
            start, end = _atom(left, minimum, maximum, field), _atom(right, minimum, maximum, field)
            if start > end: raise CronError(f"Invalid descending {field} range: {base}")
        else:
            if slash: raise CronError(f"Step syntax requires * or a range in {field}")
            start = end = _atom(base, minimum, maximum, field)
        result.update(range(start, end + 1, step))
    if not result: raise CronError(f"Empty {field} field")
    return result

def _describe(value: str, field: str) -> str:
    if value == "*": return f"any {field}"
    if value.startswith("*/"): return f"every {value[2:]} {field} units"
    return f"{field}={value}"
