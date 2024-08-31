import unittest

class TestSmartBin(unittest.TestCase):

    def test_bin_level(self):
        waste_level = 50        	
        self.assertTrue(waste_level < 100, "Bin level should be less than 100!")

    def test_empty_bin(self):
        waste_level = 0 
        self.assertEqual(waste_level, 0, "Bin should be empty")

if __name__ == '__main__':
    unittest.main()

