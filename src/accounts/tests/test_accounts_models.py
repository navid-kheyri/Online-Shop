from django.test import TestCase, Client
from ..models import CustomUser, UserImage


class TestCustomUser(TestCase):
    def setUp(self):

        self.client = Client()
        self.user_obj = CustomUser.objects.create(email='navid@gmail.com', phone_number='09121234567',
                                                  age=30, city='tehran', user_type='customer')

    def test_create_user(self):

        self.assertEqual(self.user_obj.email, 'navid@gmail.com')
        self.assertEqual(self.user_obj.phone_number, '09121234567')
        self.assertEqual(self.user_obj.age, 30)
        self.assertEqual(self.user_obj.city, 'tehran')
        self.assertEqual(self.user_obj.user_type, 'customer')


class TestUserImage(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_obj = CustomUser.objects.create(email='navid@gmail.com', phone_number='09121234567',
                                                  age=30, city='tehran', user_type='customer')
        self.image_obj = UserImage.objects.create(
            user=self.user_obj, title='logo', image='media/logo.png')

    def test_create_user_image(self):
        self.assertEqual(self.image_obj.title , 'logo')
        self.assertEqual(self.image_obj.image, 'media/logo.png')
        self.assertEqual(self.image_obj.user, self.user_obj)