from flask import Flask
import unittest

app = Flask(__name__)

@app.route('/')
def hello_sit223():
    return "Hello SIT223!"

# Unit Tests
class TestSmartBin(unittest.TestCase):

    def test_bin_level(self):
        waste_level = 50
        self.assertTrue(waste_level < 100, "Bin level should be less than 100!")

    def test_empty_bin(self):
        waste_level = 0
        self.assertEqual(waste_level, 0, "Bin should be empty")

if __name__ == '__main__':
    import sys
    if 'test' in sys.argv:
        # Run unit tests
        unittest.main()
    else:
        # Run the Flask app
        app.run(host='0.0.0.0', port=80)
