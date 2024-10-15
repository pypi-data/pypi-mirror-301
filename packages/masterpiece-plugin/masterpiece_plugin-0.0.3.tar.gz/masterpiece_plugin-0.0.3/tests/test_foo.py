import unittest

from masterpiece_plugin import Foo


class TestFoo(unittest.TestCase):
    """Unit tests for `Foo` class."""

    def test_get_classid(self):
        """Assert that the meta-class driven class initialization works."""
        classid = Foo.get_class_id()
        self.assertEqual("Foo", classid)


if __name__ == "__main__":
    unittest.main()
