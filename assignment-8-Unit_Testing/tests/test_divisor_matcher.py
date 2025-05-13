import unittest
from divisor_app.divisor_matcher import ConsecutiveDivisorMatcher

class TestConsecutiveDivisorMatcher(unittest.TestCase):

    def test_small_k(self):
        matcher = ConsecutiveDivisorMatcher(20)
        self.assertEqual(matcher.query(3), 1) 
        self.assertEqual(matcher.query(15), 2) 

    def test_multiple_values(self):
        matcher = ConsecutiveDivisorMatcher(100)
        self.assertTrue(matcher.query(20) >= 2)  
        self.assertTrue(matcher.query(100) >= matcher.query(50))

    def test_minimum_k(self):
        matcher = ConsecutiveDivisorMatcher(10)
        self.assertEqual(matcher.query(2), 0)  

    def test_invalid_query(self):
        matcher = ConsecutiveDivisorMatcher(10)
        with self.assertRaises(ValueError):
            matcher.query(20) 

if __name__ == '__main__':
    unittest.main()