import unittest
#Import our functions that we want to test
from example_function import add_two_numbers

class TestAddition(unittest.TestCase):
    def test_add_two_numbers_handles_zeros(self):
        """Test add_two_numbers handles zero values"""
        x = 0
        y = 0
        expected = 0
        observed = add_two_numbers(x,y)
        self.assertEqual(observed,expected)        

    def test_add_two_numbers_handles_negatives(self):
        """Test that add_two_numbers adds negative numbers correctly"""
        x = 40
        y = -10
        expected = 30
        observed = add_two_numbers(x,y)
        self.assertEqual(observed,expected)

#Run the tests
unittest.main()
