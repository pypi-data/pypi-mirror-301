import unittest
from src import multiply
from src.multiply.multiply_by_three import multiply_by_three


class TestMultiplyByThree(unittest.TestCase):

    def test_multiply_by_three(self):
        self.assertEqual(multiply_by_three(12), 36)


if __name__ == "__main__":
    unittest.main()
