import unittest
from studysprint import validators as v


class TestValidators(unittest.TestCase):
    def test_name_ok_and_trimmed(self):
        self.assertEqual(v.validate_name("  Python "), "Python")

    def test_name_empty_or_long(self):
        with self.assertRaises(v.ValidationError): v.validate_name("   ")
        with self.assertRaises(v.ValidationError): v.validate_name("x" * 200)

    def test_ranges(self):
        self.assertEqual(v.validate_difficulty("4"), 4)
        self.assertEqual(v.validate_quality(0), 0)
        for bad in (0, 6, "a", None):
            with self.assertRaises(v.ValidationError): v.validate_difficulty(bad)
        for bad in (-1, 6, "x"):
            with self.assertRaises(v.ValidationError): v.validate_quality(bad)
        for bad in (0, 100000, "ten"):
            with self.assertRaises(v.ValidationError): v.validate_minutes(bad)

    def test_date(self):
        self.assertEqual(v.validate_date("2026-01-31").day, 31)
        with self.assertRaises(v.ValidationError): v.validate_date("31-01-2026")


if __name__ == "__main__":
    unittest.main()
