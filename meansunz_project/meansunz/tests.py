from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client


class meansunz(TestCase):
    def test_leaderboards_contains_both_headings(self):
        response = self.client.get(reverse('leaderboards'))
        self.assertIn('Popularity score'.lower(), response.content.decode('ascii').lower())

    def test_URL(self):
        url = reverse('about')
        self.assertIn(url, '/about/')
        url = reverse('leaderboards')
        self.assertIn(url, '/leaderboards/')
        url = reverse('login')
        self.assertIn(url, '/login/')
        url = reverse('register')
        self.assertIn(url, '/register/')

    def test_login(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan', 'email': 'susan@susan.com', 'password': 'password'})
        response = c.post('/login/', {'username': 'susan', 'password': 'password'})
        code=str(response.status_code)
        self.assertIn(code, "302")

    def test_login_with_wrong_password(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan', 'email': 'susan@susan.com', 'password': 'password'})
        response = c.post('/login/', {'username': 'susan', 'password': 'wrongpassword'})
        code = str(response.status_code)
        self.assertIn(code, "200")

    def test_login_with_wrong_password(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan', 'email': 'susan@susan.com', 'password': 'password'})
        response = c.post('/login/', {'username': 'susan', 'password': 'wrongpassword'})
        code = str(response.status_code)
        self.assertIn(code, "200")

    def test_login_with_wrong_username(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan', 'email': 'susan@susan.com', 'password': 'password'})
        response = c.post('/login/', {'username': 'notsusan', 'password': 'password'})
        code = str(response.status_code)
        self.assertIn(code, "200")

    def test_double_register(self):
        c = Client()
        response = c.post('/register/', {'username': 'susan', 'email': 'susan@susan.com', 'password': 'password'})
        response = c.post('/register/', {'username': 'susan', 'email': 'susan@susan.com', 'password': 'password'})
        self.assertIn('already exists'.lower(), response.content.decode('ascii').lower())