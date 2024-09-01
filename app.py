from flask import Flask
import unittest
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello SIT223!"

# Your Python test functions
class TestSmartBin(unittest.TestCase):

    def test_bin_level(self):
        waste_level = 50
        self.assertTrue(waste_level < 100, "Bin level should be less than 100!")

    def test_empty_bin(self):
        waste_level = 0
        self.assertEqual(waste_level, 0, "Bin should be empty")


if __name__ == '__main__':
    # Check if we're running in a test environment or locally
    if os.getenv('RUN_TESTS') == '1':
        # Running the tests
        unittest.main()
    else:
        app.run(host='0.0.0.0', port=80)
