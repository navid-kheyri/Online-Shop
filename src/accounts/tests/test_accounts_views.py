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



class TestCustomRegister(TestCase):
    def setUp(self):
        self.client=Client()
        self.user = {'register-email':'navid@gmail.com','register-phone-number':'09121234567',
                                    'register-password':'pass123','register-password-2':'pass123','register-age':20,'register-city':'qom',
                                    'register-first-name':'ali','register-last-name':'alibaba'}
        self.url=reverse('accounts:register')

    def test_register_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code , 200)

    def test_register_user(self):
        response = self.client.post(self.url , self.user)
        self.assertEqual(response.status_code , 302)
        self.assertTrue(User.objects.filter(email='navid@gmail.com').exists())
    
    def test_register_email_exist(self):
        response = self.client.post(self.url , {'register-email':'navid@gmail.com','register-phone-number':'09141234567',
                                    'register-password':'pass123','register-password-2':'pass123','register-age':20,'register-city':'qom',
                                    'register-first-name':'ali','register-last-name':'alibaba'})
        self.assertEqual(response.status_code,200)
    #same for phone

    def test_register_email_exist(self):
        self.user['register-password-2']='132456789'
        response = self.client.post(self.url , self.user)
        self.assertEqual(response.status_code, 200)