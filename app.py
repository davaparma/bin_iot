from flask import Flask
import unittest

app = Flask(__name__)

# Unit tests for the Jenkinsfile
class TestSmartBin(unittest.TestCase):

    def test_bin_level(self):
        waste_level = 50        	
        self.assertTrue(waste_level < 100, "Bin level should be less than 100!")

    def test_empty_bin(self):
        waste_level = 0 
        self.assertEqual(waste_level, 0, "Bin should be empty")

# Route for running tests in the Jenkins pipeline
@app.route('/run-tests')
def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSmartBin)
    
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    output = f"Ran {result.testsRun} tests.\n"
    if result.wasSuccessful():
        output += "All tests passed successfully!"
    else:
        output += "Some tests failed."

    return output

# Route for Azure to print "Hello SIT223!"
@app.route('/')
def hello_sit223():
    return "Hello SIT223!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
