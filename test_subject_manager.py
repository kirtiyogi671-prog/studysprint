import unittest
from studysprint.database import Database
from studysprint.subject_manager import SubjectManager
from studysprint.validators import ValidationError


class TestSubjectManager(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.m = SubjectManager(self.db)

    def test_crud_subject(self):
        s = self.m.add_subject("Python")
        self.assertEqual(self.m.get_subject(s.id).name, "Python")
        self.m.rename_subject(s.id, "Python 3")
        self.assertEqual(self.m.list_subjects()[0].name, "Python 3")
        self.m.delete_subject(s.id)
        self.assertEqual(self.m.list_subjects(), [])

    def test_duplicate_subject_case_insensitive(self):
        self.m.add_subject("Maths")
        with self.assertRaises(ValidationError): self.m.add_subject("maths")

    def test_topics_and_cascade(self):
        s = self.m.add_subject("DSA")
        t = self.m.add_topic(s.id, "Heaps", 4)
        self.assertEqual(t.difficulty, 4)
        self.assertIsNone(t.next_review)
        self.m.update_difficulty(t.id, 5)
        self.assertEqual(self.m.get_topic(t.id).difficulty, 5)
        self.m.delete_subject(s.id)  # cascades
        self.assertEqual(self.m.list_topics(), [])

    def test_bad_inputs(self):
        with self.assertRaises(ValidationError): self.m.add_topic(999, "X")
        s = self.m.add_subject("A")
        with self.assertRaises(ValidationError): self.m.add_topic(s.id, "T", 9)
        self.m.add_topic(s.id, "T")
        with self.assertRaises(ValidationError): self.m.add_topic(s.id, "T")


if __name__ == "__main__":
    unittest.main()
