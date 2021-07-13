import unittest, sys

sys.path.append('../dogsarecool') # imports python file from parent directory
from main_file import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response1 = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response1.status_code, 200)


    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_dogs(self):
        response = self.app.get('/dogs', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

#    def test_captions_page(self):
#        response = self.app.get('/captions', follow_redirects=True)
#        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()