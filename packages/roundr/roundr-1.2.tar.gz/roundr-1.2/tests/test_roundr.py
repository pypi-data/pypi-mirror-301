# tests/test_roundr.py

import unittest
from roundr import round_utils 

class TestRoundUtils(unittest.TestCase):
    
    def test_round_up(self):

        self.assertEqual(round_utils(34.567, 1), 34.6)
        self.assertEqual(round_utils(349.5), 350)
        
    def test_round_down(self):

        self.assertEqual(round_utils(6.54, 1), 6.5)
        self.assertEqual(round_utils(6.55),7)
    
    def test_round_invalid_input(self):

        self.assertEqual(round_utils(6, 'e'), "Invalid input, try again!")
        self.assertEqual(round_utils('r', 3), "Invalid input, try again!")

    def test_round_with_string(self):
        
        self.assertEqual(round_utils('6.56', '1'), 6.6)
        self.assertEqual(round_utils('6.55'), 7)

if __name__ == '__main__':
    unittest.main()
