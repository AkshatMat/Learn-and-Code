import unittest
from divisor_app.divisor_counter import DivisorCounter

class TestDivisorCounter(unittest.TestCase):

    def test_known_divisors(self):
        dc = DivisorCounter(20)
        self.assertEqual(dc.get(14), 4)  
        self.assertEqual(dc.get(15), 4)  
        self.assertEqual(dc.get(16), 5)  

    def test_out_of_range(self):
        dc = DivisorCounter(10)
        with self.assertRaises(ValueError):
            dc.get(12)

    def test_min_range(self):
        dc = DivisorCounter(2)
        self.assertEqual(dc.get(1), 1)
        self.assertEqual(dc.get(2), 2)

if __name__ == '__main__':
    unittest.main()
