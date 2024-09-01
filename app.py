import sys
from flask import Flask
import unittest

app = Flask(__name__)

@app.route('/')
def hello_sit223():
    return "Howdy - SIT223!"

class TestSmartBin(unittest.TestCase):
    def test_bin_level(self):
        waste_level = 50        	
        self.assertTrue(waste_level < 100, "Bin level should be less than 100!")

    def test_empty_bin(self):
        waste_level = 0 
        self.assertEqual(waste_level, 0, "Bin should be empty")

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSmartBin)
    
    runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result = runner.run(suite)

    # Print the test results
    output = f"Ran {result.testsRun} tests.\n"
    if result.wasSuccessful():
        output += "All tests passed successfully!"
    else:
        output += "Some tests failed:\n"
        for failed in result.failures:
            output += f"{failed[0]}: {failed[1]}\n"

    print(output)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
    else:
        app.run(host='0.0.0.0', port=80)
