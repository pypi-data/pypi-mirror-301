import unittest
from src.divide.divide_by_three import divide_by_three


class TestDivideByThree(unittest.TestCase):

    def test_divide_by_three(self):
        self.assertEqual(divide_by_three(12), 4)


if __name__ == "__main__":
    unittest.main()
