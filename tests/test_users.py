import unittest, sys, os

sys.path.append('../week3website') # imports python file from parent directory
from main import app, db

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    ###############
    #### tests ####
    ###############

    def register(self, username, email, password):
        return self.app.post('/register',
                            data=dict(username=username,
                                      email=email,
                                      password=password, 
                                      confirm_password=password),
                            follow_redirects=True)

    def test_valid_user_registration(self):
        response = self.register('test', 'test@example.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[password], response.data[confirm_password]) # why won't this work
    
    def test_invalid_username_registration(self):
        response = self.register('t', 'test@example.com', 'FlaskIsAwesome')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)

    def test_invalid_email_registration(self):
        response = self.register('test2', 'test@example', 'FlaskIsAwesome')
        self.assertIn(b'Invalid email address.', response.data)
    def test_bad_password_registration(self):
        response = self.register('test3', 'tester@example.', 'abc123')
        self.assertIn(b'Invalid email address.', response.data)
    def test_good_user_registration(self):
        response = self.register('test4', 'test4@example.com', '1')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()