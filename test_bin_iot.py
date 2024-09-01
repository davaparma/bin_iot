from flask import Flask
import unittest

app = Flask(__name__)

# Your Python test functions
class TestSmartBin(unittest.TestCase):

    def test_bin_level(self):
        waste_level = 50        	
        self.assertTrue(waste_level < 100, "Bin level should be less than 100!")

    def test_empty_bin(self):
        waste_level = 0 
        self.assertEqual(waste_level, 0, "Bin should be empty")

@app.route('/')
def run_tests():
    # Running the tests and capturing the results
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSmartBin)
    
    runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result = runner.run(suite)

    # Formatting the test results as a string to display
    output = f"Ran {result.testsRun} tests.\n"
    if result.wasSuccessful():
        output += "All tests passed successfully!"
    else:
        output += "Some tests failed:\n"
        for failed in result.failures:
            output += f"{failed[0]}: {failed[1]}\n"

    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
