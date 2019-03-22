from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client

    # this test tests that the leaderboards page displays headings
class meansunz(TestCase):
    def test_leaderboards_contains_headings(self):
        response = self.client.get(reverse('leaderboards'))
        # checks at this stage
        self.assertIn('Popularity score'.lower(),
                      response.content.decode('ascii').lower())

    # This test checks the URLs that will exist for every user
    def test_URL(self):
        # tests about
        url = reverse('about')
        self.assertIn(url, '/about/')
        # tests leaderboards
        url = reverse('leaderboards')
        self.assertIn(url, '/leaderboards/')
        # tests login
        url = reverse('login')
        self.assertIn(url, '/login/')
        # tests Register
        url = reverse('register')
        self.assertIn(url, '/register/')

    # this test checks that the register and login functionality completes successfully
    def test_login(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan',
                                         'email': 'susan@susan.com',
                                         'password': 'password'})
        response = c.post('/login/', {'username': 'susan',
                                      'password': 'password'})
        code=str(response.status_code)
        # correct details returns status code 302 which this line checks
        self.assertIn(code, "302")

    # tests for incorrect password
    def test_login_with_wrong_password(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan',
                                         'email': 'susan@susan.com',
                                         'password': 'password'})
        response = c.post('/login/', {'username': 'susan',
                                      'password': 'wrongpassword'})
        code = str(response.status_code)
        # incorrect details returns status code 200 which this line checks
        self.assertIn(code, "200")

    # tests login with incorrect username
    def test_login_with_wrong_username(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan',
                                         'email': 'susan@susan.com',
                                         'password': 'password'})
        response = c.post('/login/', {'username': 'notsusan',
                                      'password': 'password'})
        code = str(response.status_code)
        # incorrect details returns status code 200 which this line checks
        self.assertIn(code, "200")

    def test_double_register(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan',
                                         'email': 'susan@susan.com',
                                         'password': 'password'})
        response = c.post('/register/', {'username': 'susan',
                                         'email': 'susan@susan.com',
                                         'password': 'password'})
        self.assertIn('already exists'.lower(), response.content.decode('ascii').lower())

    def test_double_register_login(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan',
                                         'email': 'susan@susan.com',
                                         'password': 'password'})
        response = c.post('/register/', {'username': 'susan',
                                         'email': 'thenewsusan@susan.com',
                                         'password': 'password2'})
        response = c.post('/login/', {'username': 'susan',
                                      'password': 'password2'})
        code = str(response.status_code)
        # the second account should not be created due to a conflict so
        # incorrect details returns status code 200 which this line checks
        self.assertIn(code, "200")
