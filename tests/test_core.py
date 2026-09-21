import unittest
from datetime import datetime
from cron_builder import CronError, CronExpression, build

class CronTests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(str(CronExpression.parse("*/15 9-17 * * MON-FRI")), "*/15 9-17 * * MON-FRI")

    def test_invalid(self):
        for value in ("* * * *", "60 * * * *", "*/0 * * * *"):
            with self.assertRaises(CronError):
                CronExpression.parse(value)

    def test_named_weekday(self):
        expr = CronExpression.parse("0 9 * JAN MON")
        self.assertTrue(expr.matches(datetime(2026, 1, 5, 9, 0)))
        self.assertFalse(expr.matches(datetime(2026, 1, 6, 9, 0)))

    def test_preview(self):
        runs = CronExpression.parse("*/15 * * * *").next_runs(datetime(2026, 9, 21, 10, 7), 3)
        self.assertEqual(runs[0], datetime(2026, 9, 21, 10, 15))
        self.assertEqual(runs[-1], datetime(2026, 9, 21, 10, 45))

    def test_builder(self):
        self.assertEqual(str(build("30", "8", weekday="MON-FRI")), "30 8 * * MON-FRI")

    def test_explain(self):
        self.assertEqual(CronExpression.parse("0 0 * * *").explain(), "Every day at 00:00")

if __name__ == "__main__":
    unittest.main()
