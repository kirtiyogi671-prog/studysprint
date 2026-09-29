import contextlib
import io
import unittest
from studysprint.cli import build_parser, run
from studysprint.database import Database
from studysprint.validators import ValidationError


def call(db, *argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run(build_parser().parse_args(argv), db)
    return buf.getvalue()


class TestCLI(unittest.TestCase):
    def test_end_to_end_flow(self):
        db = Database(":memory:")
        self.assertIn("Added subject #1", call(db, "add-subject", "Python"))
        self.assertIn("Added topic #1", call(db, "add-topic", "1", "Decorators", "-d", "4"))
        self.assertIn("Decorators", call(db, "due"))
        self.assertIn("Planned 30/60", call(db, "plan", "60"))
        self.assertIn("Next review", call(db, "log", "1", "30", "4"))
        self.assertIn("Nothing due", call(db, "due"))
        self.assertIn("Total study time : 30", call(db, "report"))

    def test_errors_propagate(self):
        db = Database(":memory:")
        with self.assertRaises(ValidationError):
            call(db, "log", "42", "10", "3")


if __name__ == "__main__":
    unittest.main()
