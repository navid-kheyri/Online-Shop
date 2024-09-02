from django.test import TestCase ,Client
from django.urls import reverse
from ..views import User ,CustomLoginView


class TestCustomLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = 'accounts:login'
        self.customer=User.objects.create_user(email='navid@gmail.com', phone_number='09121234567',
                                       password='123', age=30, city='tehran', user_type='customer')
        self.owner=User.objects.create_user(email='karim@gmail.com', phone_number='09131234567',
                                       password='123', age=30, city='tehran', user_type='owner')
        
    def test_login_page(self):
        response = self.client.get(reverse(self.url))
        self.assertEqual(response.status_code , 200)
        
    def test_login_customer(self):
        response = self.client.post(reverse(self.url) , {'singin-email':'navid@gmail.com','singin-password':'123'})
        self.assertEqual(response.status_code, 302)
        #  or self.assertRedirects(response, reverse('website:index'))

    def test_login_owner(self):
        response = self.client.post(reverse(self.url) , {'singin-email':'karim@gmail.com','singin-password':'123'})
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, reverse('dashboard:owner-dashboard'))

    def test_failure_login(self):
        response = self.client.post(reverse(self.url) ,{'singin-email':'javad@gmail.com','singin-password':'1243'})
        self.assertEqual(response.status_code , 200)



